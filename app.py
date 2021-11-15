from flask import Flask, request, make_response, jsonify
from pytube import YouTube, Search
from humanfriendly import format_timespan, format_size
import validators

app = Flask(__name__)

@app.route('/')
def index():
	return 'Hello there...'

@app.route('/api/ytmp4', methods=['GET', 'POST'])
def ytdl():
	url = request.args.get('url')
	res = request.args.get('res')
	resolutions = ["114p", "360p", "720p"]
	if (validators.url(url) and res is not None and len(res) and res in resolutions):
		try:
			yt = YouTube(url)
			video = yt.streams.filter(res=res, progressive=True).first()

			response = make_response(
				jsonify({
					"status": 200,
					"result": {
						"title": yt.title,
						"thumbnail": yt.thumbnail_url,
						"desc": yt.description,
						"raw_duration": yt.length,
						"duration": format_timespan(yt.length),
						"resolution": res,
						"raw_size": video.filesize,
						"size":format_size(video.filesize),
						"download_url": video.url
					}
				})
			)

			response.headers["Content-Type"] = "application/json"
			return response
		except Exception as e:
			return {
				"status": "error",
				"result": "download failed"
			}
	else:
		return {
			"status": "error",
			"result": "url or parameter invalid"
		}

@app.route('/api/ytmp3', methods=['GET', 'POST'])
def ytmp3():
	url = request.args.get('url')

	if(validators.url(url)):
		try:
			yt = YouTube(url)
			audio = yt.streams.get_audio_only()

			response = make_response(
				jsonify({
					"status": 200,
					"result": {
						"title": yt.title,
						"thumbnail": yt.thumbnail_url,
						"desc": yt.description,
						"raw_duration": yt.length,
						"duration": format_timespan(yt.length),
						"raw_size": audio.filesize,
						"size":format_size(audio.filesize),
						"download_url": audio.url
					}
				})
			)

			response.headers["Content-Type"] = "application/json"
			return response
		except Exception as e:
			return {
				"status": "error",
				"result": "download failed"
			}
	else:
		return {
			"status": "error",
			"result": "url invalid"
		}

@app.route('/api/search', methods=['GET', 'POST'])
def ytsearch():
	query = request.args.get('q')
	if (len(query)):
		try:
			ys = Search(query).results[0]
			audio = ys.streams.get_audio_only()
			response = make_response(
				jsonify({
					"status": 200,
					"result": {
					    "url": "https://youtu.be/" + ys.video_id,
						"title": ys.title,
						"thumbnail": ys.thumbnail_url,
						"desc": ys.description,
						"raw_duration": ys.length,
						"duration": format_timespan(ys.length),
						"raw_size": audio.filesize,
						"size":format_size(audio.filesize),
						"download_url": audio.url
					}
				})
			)
			response.headers["Content-Type"] = "application/json"
			return response
		except Exception as e:
			return {
				"status": "error",
				"result": "download failed"
			}
	else:
		return {
			"status": "error",
			"result": "parameter is empty"
		}

if __name__ == '__main__':
	app.run(debug = True)
