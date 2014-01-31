cursor = db.collection.aggregate( 
  {
    $match: {
      "coordinates.coordinates": { $exists: true, $ne: '' }
    }
  },
  {
    $group: {
      _id: "$id",
      location: { $addToSet: "$coordinates.coordinates" }
    }
  }
);

cursor.result.forEach(function(tweet) {
    print(tweet._id+","+tweet.location.join(' '));
});

