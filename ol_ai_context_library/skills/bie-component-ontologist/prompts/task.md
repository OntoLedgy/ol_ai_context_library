You are operating in **{{ mode }}** mode.
{% if mode == "review" %}
Target domain path: `{{ target_path }}`

Read all files under the target path using the filesystem tool, then follow the Review Mode workflow from your instructions.
{% endif %}
{% if mode == "design" %}
Domain description:
{{ domain_description }}

Follow the Design Mode workflow from your instructions.
{% endif %}
