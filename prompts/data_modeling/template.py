"""Generate data modeling prompts from a template."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, TYPE_CHECKING

from .formatters import (
    format_corrections,
    format_data_dictionary,
    format_data_model,
    format_discovery,
    format_errors,
    format_nodes,
    format_use_cases,
    format_valid_columns,
)

if TYPE_CHECKING:
    from ol_ai_services.graph_rag.orchestrators.neo4j_runway.utils.data.data_dictionary.data_dictionary import DataDictionary
    from ol_ai_services.graph_rag.orchestrators.neo4j_runway.models.core.data_model import DataModel
    from ol_ai_services.graph_rag.orchestrators.neo4j_runway.models.core.node import Nodes


def create_data_modeling_prompt(
    prefix: str,
    valid_columns: Dict[str, Any],
    rules: str,
    multifile: bool,
    data_model_as_yaml: bool = False,
    discovery: Optional[str] = None,
    data_dictionary: Optional["DataDictionary"] = None,  # type: ignore
    errors: Optional[List[str]] = None,
    corrections: Optional[str] = None,
    data_model: Optional["DataModel"] = None,  # type: ignore
    nodes: Optional["Nodes"] = None,  # type: ignore
    use_cases: Optional[List[str]] = None,
    data_model_format: Optional[str] = None,
    retry_prompt: bool = False,
    suffix: Optional[str] = None,
) -> str:
    res = prefix + " "
    if discovery is not None:
        res += format_discovery(discovery)
    if data_dictionary is not None:
        res += format_data_dictionary(
            data_dictionary=data_dictionary, multifile=multifile
        )
    res += format_valid_columns(valid_columns=valid_columns)
    if errors is not None:
        res += format_errors(errors=errors)
    if corrections is not None:
        res += format_corrections(corrections=corrections)
    if data_model is not None:
        res += format_data_model(data_model=data_model, yaml_format=data_model_as_yaml)
    if nodes is not None:
        res += format_nodes(nodes=nodes, retry_prompt=retry_prompt)
    if use_cases is not None:
        res += format_use_cases(use_cases=use_cases)
    res += rules
    if data_model_format is not None:
        res += "\n" + data_model_format
    if suffix is not None:
        res += "\n" + suffix

    return res
