map = function() {
    if (!this.entities.hashtags) {
        return;
    }

    for (index in this.entities.hashtags) {
        emit(this.entities.hashtags[index].text, 1);
    }
};

reduce = function(key, value) {
    var count = 0;
    for (index in value) {
        count += value[index];
    }
    return count;
};

result = db.runCommand(
    {
        "mapreduce" : "collection",
        "map" : map,
        "reduce" : reduce,
        "out" : "hashtags"
    }
);

cursor = db.hashtags.find().sort( { "value": -1 } );
cursor.forEach(function(tweet) {
  printjson(tweet);
});