from cloud_dfs import create_app

app = create_app()
#app.run(host='0.0.0.0')
app.run(host='0.0.0.0', threaded=False, processes=1, use_reloader=False, port=9602)