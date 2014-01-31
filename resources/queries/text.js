map = function() {
    if (!this.text || this.text.length == 0 || this.lang != 'en') {
        return;
    }
    // Replace newlines with blank spaces
    this.text = this.text.replace(/(\r\n|\n|\r)/gm,' ');
    // Delete "RT" and urls "http://any_url"
    this.text = this.text.replace(/(RT |http:[\w\.\/]+)/gm,'');

    groups = this.text.match(/[A-Za-z]+/gm);
    if (!groups || groups.length == 0){
        return;
    }

    key = groups.join(' ');

    emit(key.toLowerCase(),1); 
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
        "out" : "tweet_text"
    }
);

cursor = db.tweet_text.find().sort( { "value": -1 } );
cursor.forEach(function(tweet) {
    print(tweet._id);
});