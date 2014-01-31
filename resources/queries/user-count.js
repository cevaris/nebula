cursor = db.collection.aggregate( 
  {
    $group: {
      _id: "$user.id",
      tweet_count: { $sum: 1 }
    }
  },
  {
    $sort : { tweet_count : -1 }
  }
);

printjson(cursor);
