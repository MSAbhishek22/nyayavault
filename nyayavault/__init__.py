"""NyayaVault package: grounded legal research over a verified corpus."""

from .agent import LegalAgent, LegalAnswer
from .config import NyayaVaultConfig, config_from_env

__all__ = ["LegalAgent", "LegalAnswer", "NyayaVaultConfig", "config_from_env"]
