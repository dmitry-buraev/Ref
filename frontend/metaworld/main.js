define(
[
    'dijit/layout/BorderContainer',
    'dijit/layout/ContentPane',
    'dojo/store/JsonRest',
    'dijit/Tree',
    'metaworld/bar',
    'metaworld/SelectedItemPane'
],

function(BorderContainer, ContentPane, JsonRest, Tree, Bar, SelectedItemPane)

{
    var app = {
        init: function() {
            var self = this;

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
                    return object.is_group === true;
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

            var tree = new Tree({
                region: 'left',
                model: refStore,
                showRoot: false,
                splitter: true,
                'class': 'tree'
            });
            layout.addChild(tree);

            var main = new BorderContainer({
                region: 'center',
                'class': 'main'
            });

            main.addChild(new Bar({
                region: 'top',
                'class': 'main-bar'
            }));

            var selectedItemPane = this.selectedItem = new SelectedItemPane({
                region: 'center',
                store: refStore
            });
            main.addChild(selectedItemPane);

            layout.addChild(main);

            layout.startup();

            tree.on('click', function(clickedItem) {
                var id = clickedItem.id;
                self.selectedItem.set('itemId', id);
            });

            console.log('app initialized');
        },

        test: function() {
            return 'ok';
        }
    };
    return app;
});
