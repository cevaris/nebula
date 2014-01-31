map = function() {
    if (!this.entities.hashtags || this.entities.hashtags.length == 0) {
        return;
    }

    itemset = new Array();
    for (index in this.entities.hashtags) {
        itemset.push(this.entities.hashtags[index].text.toLowerCase()); 
    }

    set = itemset.sort();
    key = set.join();

    emit(key, 1);
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
        "out" : "hashtag_itemsets"
    }
);

cursor = db.hashtag_itemsets.find().sort( { "value": -1 } );
cursor.forEach(function(tweet) {
    print(tweet._id);
});