run:
	@uvicorn workoutapi.main:app --reload

create-migrations:
	@set PYTHONPATH=%PYTHONPATH%;. && alembic revision --autogenerate -m "$(d)"

run-migrations:
	@set PYTHONPATH=%PYTHONPATH%;. && alembic upgrade head
	