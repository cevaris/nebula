cursor = db.collection.aggregate( 
  {
    $match: {
      "user.location": { $exists: true, $ne: '' }
    }
  },
  {
    $group: {
      _id: "$user.location",
      location_count: { $sum: 1 }
    }
  },
  {
    $match: {
      location_count: {$gte: 9}
    }
  },
  {
    $sort : { location_count : -1 }
  }
);

printjson(cursor);
