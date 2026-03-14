window.{{ group }} = [
  {% for items in data %}{{"{"}}{% for key, value in items.items() %}
      {{key}}: {{value}}{% if not loop.last %},{% endif %}{% endfor %}
  {{"}"}}{% if not loop.last %},{% endif %}{% endfor %}
];