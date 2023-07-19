import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Layouts 1.2
import QtQuick.Controls 2.15

import "../qml_pages"
import "../qml_components"
import ".."


Item {
    id: stageSetupView
    
    property int fixture_id
    property int fixture_library_id

    Connections {
        target: dmxListQmlPresentationModel  
    }

    // Header
    Rectangle {
        id: fixturePatchHeader
        x: 5
        y: 0
        width: 1045
        height: 50
        color: "orange"
        
        Text {
            id: fixturePatchHeaderText
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
            text: "Stage View"
            font.family: "TW Cen MT"
            font.pixelSize: 23
            font.styleName: "Bold"
            color: "black"
        }
    }

    Item {
        id: wrapper
        width: 1065
        height: 800
        x: -5
        y: 40

        // Rectangle {
        //     id: background
        //     anchors.fill: parent
        //     color: "orange"
        // }
        
        
        // Drop Area / Stage View
        DropArea {
            id: dropArea
            anchors.fill: parent
            anchors.margins: 10

            // Running at the beginning of the program -> create the tiles for the fixtures already in stage view
            Component.onCompleted: {
                // create/paint the already in stage view existing fixtures
                                
                var all_fixtures_in_stage_view = stageViewQmlPresentationModel.get_all_fixtures_in_stage_view()

                for (var i = 0; i < all_fixtures_in_stage_view.length; i++) {
                    // create the tile
                    var component
                    var movableFixtureItem
                    component = Qt.createComponent("MovableFixtureItem.qml")
                    movableFixtureItem = component.createObject(dropArea)
                    
                    // get the Fixture_Id of the dragged fixture
                    fixture_id = all_fixtures_in_stage_view[i][0]
                    fixture_library_id = all_fixtures_in_stage_view[i][1]

                    // add properties to the tile
                    movableFixtureItem.x = all_fixtures_in_stage_view[i][2][0]
                    movableFixtureItem.y = all_fixtures_in_stage_view[i][2][1]
                    movableFixtureItem.fixture_id = fixture_id

                    // find symbol for fixture id
                    movableFixtureItem.image_source = stageViewQmlPresentationModel.get_matching_symbol_number(fixture_library_id)

                    // console log for debugging
                    console.log("Created tile with id: " + fixture_id)

                }
            }

            
            Rectangle {
                id: dropRectangle
                anchors.fill: parent
                color: "#2a2a2a"
                states: [
                    State {
                        when: dropArea.containsDrag
                        PropertyChanges {
                            target: positionTempText
                            text: "x: " + dropArea.drag.x + " y: " + dropArea.drag.y
                        }
                    }
                ]
            }

            // Running when a fixture is added to the stage view           
            onDropped: {
                console.log("dropped")
                stageViewQmlPresentationModel.add_fixture_to_stage_view_wish(dropArea.drag.x, dropArea.drag.y)

                // create the tile
                var component
                var movableFixtureItem
                component = Qt.createComponent("MovableFixtureItem.qml")
                movableFixtureItem = component.createObject(dropArea)
                
                // get the Fixture_Id of the dragged fixture
                fixture_id = drag.source.active_fixture
                fixture_library_id = drag.source.active_fixture_library_id

                // add properties to the tile
                movableFixtureItem.x = dropArea.drag.x
                movableFixtureItem.y = dropArea.drag.y
                movableFixtureItem.fixture_id = fixture_id

                // find symbol for fixture id
                movableFixtureItem.image_source = stageViewQmlPresentationModel.get_matching_symbol_number(fixture_library_id)
            }
            
            // Deleting Drop Area
            Rectangle{
                id: deletingArea
                width: 100
                height: 95
                x: 0
                y: 780
                color: "red"
                border.color: "black"
                border.width: 5

                Image {
                    id: trashCan
                    source: "../res/trash_can.png"
                    anchors.centerIn: parent
                    width: 40   
                    height: 40
                }

            }
        }

        
        
    }    
}
