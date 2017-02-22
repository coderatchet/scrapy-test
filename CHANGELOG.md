## 0.1.1
- Feature: Added Merging proxy dictionary
- Patch: removed unecessary shebangs at start of files
- Patch: Added copyright to files.

## 0.2.0
- Feature: Added ability to read config from json file.
- Feature: Added ability to add environment specific configuration.
- Feature: Article stores DateTime
- Feature: Added spider to crawl news website theguardian.com.au
- Feature: Documents are stored in mongodb for later retrieval 
- Fix: Cleaned test data
- Fix: Changed db orm to use mongoengine

## 0.3.1
- Feature: Added rudimentary cmd line `scrapytest.sh`. Call `./scrapytest.sh -h` for more info.
- Util: Added merge_dict function to utils. useful for loading merged config json.
- Fix: removed beautifulsoup4 (not being used, so only patch)
- Fix: config now correctly merges environment json into main config
- Fix: improved author tag parsing in guardian articles