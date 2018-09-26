# MyGallery

Our UI Gallery website is https://ui-gallery-extension.herokuapp.com/.

## Python Files

All these python files are used to created some related documents like widgets or json file which will be used later in the UI project.

BestScreenshot.py : procedure wisgets and json file which would be used in searching part in our website.
BestCompany.py : procedure wisgets and json file which would be used in comparison part in our website.


## Deployment

Deployment is quite simple. You only need to install python3 and it's done.

However, there is no data set in this repository because it is too large (140GB). If you want to run our code, you can contact me and get some data.

The data stored in MongoDB is within the `widgets` collection with the following item structure:

widgets.json / company.json (is also in our respository)
```json
{ 
  "_id" : ObjectId("5ac23b7e27bc4099fb9fb172"), 
  "name" : "clipping-1265", 
  "clickable" : "true", 
  "color" : "Black", 
  "content-desc" : "", 
  "coordinates" : { 
    "from" : [ 4, 958 ], 
    "to" : [ 796, 1018 ] 
  }, 
  "dimensions" : { 
    "height" : 60, 
    "width" : 792 
  }, 
  "focusable" : "true", 
  "leaf" : true, 
  "package_name" : "com.plexnor.gravityscreenofffree", 
  "text" : "Activer cette option permet une réponse plus rapide. Mais si vous souhaitez éteindre l’écran manuellement par le bouton d’arrêt cette option peut interférer avec votre action et l’écran peut se rallumer.", 
  "widget_class" : "CheckBox", 
  "application_name" : "Gravity Screen - On/Off", 
  "downloads" : "1,000,000 - 5,000,000", 
  "url" : "https://play.google.com/store/apps/details?id=com.plexnor.gravityscreenofffree", 
  "src" : "/mnt/UIXML/top_10000_google_play_20170510_cleaned/com.plexnor.gravityscreenofffree_310010-output/stoat_fsm_output/ui/S_743", 
  "category" : "TOOLS",
  "Developer" : "Google_Inc"
}
```
## Authors

Yuyang Wang
Email: Tony970412@gmail.com
