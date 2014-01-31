map = function() {
    if (!this.entities.urls || this.entities.urls.length == 0) {
        return;
    }

    itemset = new Array();
    for (index in this.entities.urls) {
        emit(this.entities.urls[index].url,1);
    }
};

reduce = function(previous, current) {
    var count = 0;
    for (index in current) {
        count += current[index];
    }
    return count;
};

result = db.runCommand(
    {
        "mapreduce" : "collection",
        "map" : map,
        "reduce" : reduce,
        "out" : "urls"
    }
);

cursor = db.urls.find().sort( { "value": -1 } );
cursor.forEach(function(tweet) {
    print(tweet.value + ",\""+tweet._id+"\"");
});
