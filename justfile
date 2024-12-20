run day part:
  uv run main.py --day {{day}} --part {{part}} --input ./inputs/{{day}}

init day:
  cp common/day_template.py solutions_2024/day_{{day}}.py
  touch inputs/test_{{day}}
  touch inputs/{{day}}
