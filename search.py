import scrapetube

class Search:
    def __init__(self, query):
        self.query = query
        self.videos = scrapetube.get_search(query=query,results_type="video")

    def getNext(self):
        for video in self.videos:
            videoFiltered = {}

            if "badges" in video:
                for label in video["badges"]:
                    if label["metadataBadgeRenderer"]["label"] == "LIVE":
                        return self.getNext()

            videoFiltered["id"] = video["videoId"]
            videoFiltered["thumbnail"] = video["thumbnail"]["thumbnails"][-1]["url"]
            videoFiltered["title"] = video["title"]["runs"][0]["text"]
            videoFiltered["length"] = video["lengthText"]["simpleText"]
            videoFiltered["views"] = video["shortViewCountText"]["simpleText"]

            videoFiltered["released"] = ""
            if "publishedTimeText" in video: videoFiltered["released"] = " · " + video["publishedTimeText"]["simpleText"]

            videoFiltered["description"] = ""
            if "detailedMetadataSnippets" in video : videoFiltered["description"] = video["detailedMetadataSnippets"][0]["snippetText"]["runs"][0]["text"]

            videoFiltered["isSubtitle"] = False
            if "badges" in video:
                for label in video["badges"]:
                    if label["metadataBadgeRenderer"]["label"] == "CC":
                        videoFiltered["isSubtitle"] = True
                        break

            videoFiltered["owner"] = video["ownerText"]["runs"][0]["text"]
            videoFiltered["ownerId"] = video["ownerText"]["runs"][0]["navigationEndpoint"]["browseEndpoint"]["browseId"]
            videoFiltered["ownerThumbnail"] = video["channelThumbnailSupportedRenderers"]["channelThumbnailWithLinkRenderer"]["thumbnail"]["thumbnails"][-1]["url"]
            
            return videoFiltered