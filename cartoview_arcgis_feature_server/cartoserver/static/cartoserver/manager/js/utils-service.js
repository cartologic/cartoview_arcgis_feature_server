app.factory('utils', function () {
  return {
    // Util for finding an object by its 'id' property among an array
    findById: function findById(arr, id) {
      var found = null;
      angular.forEach(arr, function(item,index){
        if(item.id == id) {
          found = item;
          return false;
        }
      })
      return found;
    },
    find: function(arr, val, field) {
      var found = null;
      angular.forEach(arr, function(item,index){
        if(item[field] == val) {
          found = item;
          return false;
        }
      })
      return found;
    },
    // Util for returning a random key from a collection that also isn't the current key
    newRandomKey: function newRandomKey(coll, key, currentKey){
      var randKey;
      do {
        randKey = coll[Math.floor(coll.length * Math.random())][key];
      } while (randKey == currentKey);
      return randKey;
    }
  };
});
