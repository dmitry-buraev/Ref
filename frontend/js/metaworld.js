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
                content: 'MetaWorld'
            }));

            var refStore = new JsonRest({
                target: '/refs/',

                mayHaveChildren: function(object) {
                    return object.is_leaf !== true;
                },

                getChildren: function(object, onComplete, onError) {
                    this.get(object.id).then(function(fullObject) {
                        object.children = fullObject.children;
                        onComplete(fullObject.children);
                    }, function(error) {
                        console.error(error);
                    });
                },

                getRoot: function(onItem, onError) {
                    this.get('root').then(onItem, onError);
                },

                getLabel: function(object) {
                    return object.name;
                }
            });

            layout.addChild(new Tree({
                region: 'left',
                model: refStore,
                showRoot: false,
                splitter: true,
                'class': 'tree'
            }));

            layout.addChild(new ContentPane({
                region: 'center',
                content: 'stub',
                'class': 'main'
            }));

            layout.startup();

            console.log('app initialized');
        },

        test: function() {
            return 'ok';
        }
    };
    return app;
});
