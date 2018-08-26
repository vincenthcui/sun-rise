from app import app


@app.task
def test_print():
    print 'test_print'
