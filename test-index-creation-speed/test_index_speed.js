var indexStart = Date.now();
db.test.createIndex({"name"});
var indexEnd = Date.now();
var indexSecondsElapsed = (indexEnd - indexStart)/1000;
print("index creation time:", indexSecondsElapsed);
