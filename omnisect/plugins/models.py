from dataclasses import dataclass, field
from typing import Any, Literal

from openai import BaseModel
from pydantic import Field

from src.proxies.llm_provider_proxy import LlmProviderProxy
from src.proxies.transcriber_proxy import TranscriberProxy


@dataclass
class PluginRunTimeOption:
    main: str
    tests: list[str] | None


@dataclass
class DependencyModule:
    name: str
    version: str

    def __str__(self) -> str:
        return f"{self.name}=={self.version}"


@dataclass
class SchemaField:
    type: Literal["string", "integer", "number", "boolean", "array", "object", "enum"]
    name: str | None = None
    description: str | None = None
    required: bool = True
    enum: list[Any] | None = None
    items: list["SchemaField"] | None = None
    properties: list["SchemaField"] | None = None

    def to_text(self, indent: int = 2) -> str:
        pad = " " * indent
        text = f"{pad}- {self.name or '<unnamed>'}: {self.type}"
        if self.enum:
            text += f" (one of {self.enum})"
        if self.description:
            text += f"  # {self.description}"
        if self.items:
            for item in self.items:
                text += "\n" + item.to_text(indent + 2)
        if self.properties:
            for prop in self.properties:
                text += "\n" + prop.to_text(indent + 2)
        return text


@dataclass
class Schema:
    fields: list[SchemaField] = field(default_factory=list)

    def to_text(self) -> str:
        return "\n".join(f.to_text() for f in self.fields)


@dataclass
class ValidationRule:
    field: str
    rule_type: str
    expected: Any
    subfield: str | None = None

    def to_text(self) -> str:
        if self.subfield:
            return f"- {self.field}.{self.subfield}: {self.rule_type} → {self.expected}"
        return f"- {self.field}: {self.rule_type} → {self.expected}"


@dataclass
class PluginInstructionSecurityExceptions:
    trigger: str
    allow: str

    def to_text(self) -> str:
        return f"- If '{self.trigger}', then allow: {self.allow}"


@dataclass
class PluginInstructionInputSchema:
    type: Literal["json", "text", "file"]
    schema: Schema
    validation_rules: list[ValidationRule] = field(default_factory=list)

    def to_text(self) -> str:
        parts = [f"Input type: {self.type}"]
        if self.schema.fields:
            parts.append("Schema:")
            parts.append(self.schema.to_text())
        if self.validation_rules:
            parts.append("Validation rules:")
            parts.append(
                "Validation rules are very important and it is very important to follow them. if validation is violated, the user should be informed"
            )
            parts.extend([vr.to_text() for vr in self.validation_rules])
        return "\n".join(parts)


@dataclass
class PluginInstructionSecurity:
    guidelines: list[str]
    exceptions: list[PluginInstructionSecurityExceptions]

    def to_text(self) -> str:
        text = "Security guidelines:\n"
        for g in self.guidelines:
            text += f"- {g}\n"
        if self.exceptions:
            text += "Exceptions:\n"
            for ex in self.exceptions:
                text += ex.to_text() + "\n"
        return text.strip()


@dataclass
class PluginInstructions:
    """Instructions for LLMs"""

    description: str
    steps: list[str]
    input: PluginInstructionInputSchema
    requirements: list[str]
    security: PluginInstructionSecurity

    def to_text(self, plugin_web_id: str, plugin_name: str = None) -> str:
        parts = []
        parts.append(
            f"Plugin web_id: {plugin_web_id}\n👉 This web_id must always be used when calling the function\ninvoke_plugin_api_plugins_v1__web_id__post.\nReplace <web_id> in the function name with syllabus-weaver."
        )
        parts.append(
            f"Special instructions {'for the ' + plugin_name if plugin_name else ''}:"
        )
        parts.append(f"Description:\n{self.description}\n")
        if self.steps:
            parts.append("Steps:")
            for i, step in enumerate(self.steps, 1):
                parts.append(f"{i}. {step}")
        if self.input:
            parts.append("\nInput:")
            parts.append(self.input.to_text())
        if self.requirements:
            parts.append("\nRequirements:")
            for req in self.requirements:
                parts.append(f"- {req}")
        if self.security:
            parts.append("\n" + self.security.to_text())
        return "\n".join(parts)


@dataclass
class PluginConfig:
    name: str
    alias: str
    creator: str
    runtime: PluginRunTimeOption
    repository: str
    description: str
    version: str
    requirements: list[DependencyModule] | None = None
    instructions: PluginInstructions | None = None


@dataclass
class Meta:
    web_id: str
    name: str
    description: str
    version: str
    creator: str
    instructions: PluginInstructions | None = None

    def __str__(self) -> str:
        return f"{self.name}: {self.version}"


@dataclass
class PluginInput:
    text: str | None = None
    language: str = Field(default="russian")
    data: dict[str, Any] | None = None


class PluginOutput(BaseModel):
    text: str | None = None
    file_path: str | None = None


@dataclass
class PluginServices:
    transcriber_proxy: TranscriberProxy
    llm_provider_proxy: LlmProviderProxy
