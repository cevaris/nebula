cursor = db.collection.aggregate( 
  {
    $match: {
      "retweeted_status.retweet_count": { $gt: 0 }
    }
  },
  {
    $group: {
      _id: "$retweeted_status.id_str",
      retweet_count: { $max: "$retweeted_status.retweet_count"  },
      text: { $addToSet: "$retweeted_status.text"  },
      user: { $addToSet: "$retweeted_status.user.id"  }
    }
  },
  {
    $sort : { retweet_count : -1 }
  }
);

printjson(cursor);
