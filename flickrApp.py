import flickrapi
from datetime import datetime

api_key = "xxxxx"
api_secret = "xxxxx"

flickr = flickrapi.FlickrAPI(
    api_key, api_secret, store_token=True, format="parsed-json"
)
flickr.authenticate_via_browser(perms="delete")

per = 500 # size of a "page" of results

# a list we'll build of all our photos
photos = []

# page through all our photos (there's almost 10,000)
for page in range(1, 20):
    interesting = flickr.photos.getPopular(
        sort="interesting",
        extras="date_upload, views, owner_name",
        per_page=per,
        page=page,
    )

    i = page * per
    for photo in interesting["photos"]["photo"]:
        photos = photos + [int(photo["id"])]
        i = i + 1
        print(
            i,
            int(photo["id"]),
            photo["title"],
            datetime.fromtimestamp(int(photo["dateupload"])),
            photo["views"],
        )

# go through and delete a bunch, but keeping in mind that there's at least 1000 left
for c in range(1, 500):
    target = photos.pop()
    print(len(photos), " photos remaining.", "     deleting ", target)
    print(flickr.photos.delete(photo_id=target))
    if len(photos) < 1001:
        print("STOP!! ONLY 1000 left!")
        break

print(len(photos), " left.")
