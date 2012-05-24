define(
[
       'dijit/layout/BorderContainer',
       'dijit/layout/ContentPane',
       'dojo/store/JsonRest',
       'dijit/Tree'
],

function(BorderContainer, ContentPane, JsonRest, Tree)

{
    var app = {
        init: function() {
            var layout = new BorderContainer({
                design: 'headline'
            }, 'app-layout');

            layout.addChild(new ContentPane({
                region: 'top',
                splitter: true,
                content: 'MetaWorld'
            }));

            layout.startup();

            console.log('app initialized');
        }
    };
    return app;
});
