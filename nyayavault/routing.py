"""NyayaVault routing: model choice, fallback, per-run budget.

Same shape as the BharatCode sibling: the primary model is tried
first, the fallback model is tried once on failure, the per-run
budget counts attempts (not tokens), and refusal never costs a call.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .config import NyayaVaultConfig
from .llm import BharatCodeProvider, MockProvider, ProviderResult


@dataclass
class RoutingDecision:
    """Which model was used, why, and what else was tried."""

    model: str
    reason: str
    attempted: list[str]
    fallback_used: bool
    provider: str = "mock"


@dataclass
class RoutingLedger:
    """A per-run record of routing: attempted models + call count."""

    attempted_models: list[str] = field(default_factory=list)
    fallback_used: bool = False
    calls_used: int = 0
    cap: int = 10
    exhausted: bool = False


def choose_primary_model(config: NyayaVaultConfig) -> RoutingDecision:
    """Pick the primary model before any call is made."""
    if config.mock_mode:
        return RoutingDecision(
            model="mock-extractive",
            reason="No BHARATCODE_API_KEY set — mock extractive provider.",
            attempted=[],
            fallback_used=False,
            provider="mock",
        )
    return RoutingDecision(
        model=config.model,
        reason="Primary BharatCode model configured.",
        attempted=[],
        fallback_used=False,
        provider="bharatcode",
    )


def run_with_fallback(
    config: NyayaVaultConfig,
    question: str,
    context: str,
    language: str,
    ledger: RoutingLedger,
) -> tuple[ProviderResult, RoutingDecision]:
    """Ask the primary model; on failure, try the fallback once.

    The budget counts attempts: each provider call costs 1 unit,
    whether it succeeds or fails. When the cap is reached the run
    refuses with a budget message instead of calling anything.
    """
    decision = choose_primary_model(config)
    if ledger.calls_used >= ledger.cap:
        ledger.exhausted = True
        raise RuntimeError("LLM call budget for this run exceeded")
    attempted = list(decision.attempted)
    if config.mock_mode:
        attempted.append("mock-extractive")
        ledger.attempted_models = attempted
        ledger.calls_used += 1
        result = MockProvider().ask(question, context, language)
        return result, RoutingDecision(
            model="mock-extractive",
            reason="Mock extractive provider (no key configured).",
            attempted=attempted,
            fallback_used=False,
            provider="mock",
        )
    primary = BharatCodeProvider(config)
    attempted.append(config.model)
    ledger.attempted_models = attempted
    ledger.calls_used += 1
    try:
        result = primary.ask(question, context, language)
        return result, RoutingDecision(
            model=config.model,
            reason="Primary model succeeded.",
            attempted=attempted,
            fallback_used=False,
            provider="bharatcode",
        )
    except RuntimeError:
        if ledger.calls_used >= ledger.cap:
            ledger.exhausted = True
            raise
        fallback = BharatCodeProvider(
            NyayaVaultConfig(
                corpus_root=config.corpus_root,
                base_url=config.base_url,
                api_key=config.api_key,
                model=config.fallback_model,
                fallback_model=config.fallback_model,
                daily_call_cap=config.daily_call_cap,
                mock_mode=False,
                port=config.port,
                host=config.host,
            )
        )
        attempted.append(config.fallback_model)
        ledger.attempted_models = attempted
        ledger.fallback_used = True
        ledger.calls_used += 1
        result = fallback.ask(question, context, language)
        return result, RoutingDecision(
            model=config.fallback_model,
            reason="Primary model failed; fallback model succeeded.",
            attempted=attempted,
            fallback_used=True,
            provider="bharatcode",
        )
