
push:
	git add .
	git commit -m "${message}"
	git push 

run:
	uvicorn main:app --reload