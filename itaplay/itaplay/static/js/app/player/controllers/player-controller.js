
function AllPlayerController($scope, $http, $location) {


  $scope.init = function(){
    $scope.status = false;
    $http.get("player/player_view/").then(function (response) {
      $scope.players = response.data;
     }, function(response) {
          console.log(response);
        $scope.data = "Something went wrong";
    });
    $scope.delete = function(player){
        $http.delete("player/delete_player/"+player.pk, {"pk": player.pk}).then(function (player) {
          $location.path('/#/player');
        },function (player) {
            $location.path('/#/player');
        }); 
     };
  };
        $scope.changeStatus = function(player){
    $scope.status = !$scope.status;
    player.player_status = true;
    $http.post("player/player_view/", player).success(function (player) {
          $location.path('/#/player');
  });
  };
             };  
   



function PlayerAddController($scope, $http,  $location) {
  $scope.initadd = function(){
    $scope.save = function (player){
      $http.post("player/player_view/", player).success(function (player) {
        $location.path('/#/player');
      });
    };        
  };
};

function PlayerController($scope, $http, $routeParams,  $location) {
  var id = $routeParams.id;
  $scope.initplay = function(){
    $http.get("player/current_player_view/"+id).then(function (response) {
      $scope.player = response.data.player;
    }, function(response) {
          console.log(response);
          $scope.data = "Something went wrong";
      });
      $scope.delete_current = function(player){
        $http.delete("player/delete_player/"+id, {"pk":id}).then(function (player) {
          $location.path('/#/player');
        }, function (player) {
            $location.path('/#/player');
        });
      };      
      $scope.update = function(player){
        $http.post("player/player_view/", player).success(function (player) {
          $location.path('/#/player');
        });
      };      
  };
};

