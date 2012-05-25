define(["doh/runner", 'metaworld'], function(doh, app){

    doh.register("MyTests", [
        function assertTrueTest(){
            doh.assertTrue(true);
            doh.assertTrue(1);
            doh.assertTrue(!false);
        },

        function testApp() {
            doh.is('ok', app.test());
        }
    ]);

});
