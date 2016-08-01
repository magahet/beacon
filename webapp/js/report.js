(function () {
'use strict';

angular
  .module('gps', [])
  .controller('Report', Report);

Report.$inject = ['$http', '$location', '$timeout'];

function Report($http, $location, $timeout) {

  var vm = this;
  vm.data = [];
  vm.lastUpdated = Date.now();
  //a clearer visual connection on how is defined on the view
  var key = $location.search().key

  updateLogs(0);

  function updateLogs(waitTime) {
    var timer = $timeout(function () {}, waitTime);

    timer.then(function () {
        $http({
            method: 'GET',
            url: "report.cgi",
            params: {key: key}
        }).success(function (data, status, headers, config) {
            if (data.status == 'ok') {
                vm.data = data.data;
                console.log(vm.data);
                vm.lastUpdated = Date.now();
            }
            updateLogs(60000);
        }).error(function (data, status, headers, config) {
            // something went wrong :(
        });
    }, function () {
        //console.log("Timer rejected!");
    });
  }
}

})();
