import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Layouts 1.2
import QtQuick.Controls 2.15

import "../qml_pages"
import "../qml_components"
import ".."


Item {
    id: stageSelectingView
    
    property int fixture_id
    property int fixture_library_id

    property string cueId: "1"
    property string cueName: "Cue X"
    property string cueGroup: "1"

    Connections {
        target: cueListQmlPresentationModel  
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
        width: 1045
        height: 800
        x: 5
        y: 50
        Rectangle {
            id: view
            anchors.fill: parent
            color: "#2a2a2a"
            // Running at the beginning of the program -> create the tiles for the fixtures in stage view
            Component.onCompleted: {
                // clear seletions list
                stageViewQmlPresentationModel.clear_selected_fixtures_list()

                // create/paint the in stage view existing fixtures      
                var all_fixtures_in_stage_view = stageViewQmlPresentationModel.get_all_fixtures_in_stage_view()
                for (var i = 0; i < all_fixtures_in_stage_view.length; i++) {
                    // create the tile
                    var component
                    var fixedFixtureItem
                    component = Qt.createComponent("FixedFixtureItem.qml")
                    fixedFixtureItem = component.createObject(view)
                    
                    // get the Fixture_Id of the dragged fixture
                    fixture_id = all_fixtures_in_stage_view[i][0]
                    fixture_library_id = all_fixtures_in_stage_view[i][1]

                    // add properties to the tile
                    fixedFixtureItem.x = all_fixtures_in_stage_view[i][2][0]
                    fixedFixtureItem.y = all_fixtures_in_stage_view[i][2][1]
                    fixedFixtureItem.fixture_id = fixture_id

                    // find symbol for fixture id
                    fixedFixtureItem.image_source = stageViewQmlPresentationModel.get_matching_symbol_number(fixture_library_id)

                    // console log for debugging
                    console.log("Created tile with id: " + fixture_id)
                }
            }

            // Add to cue list button
            Rectangle{
                id: addToCueListButton
                width: 100
                height: 95
                x: 0
                y: 800
                color: "green"
                border.color: "black"
                border.width: 5

                MouseArea{
                    anchors.fill: parent

                    onClicked: {
                        // open popup to select cue id and name
                        createCuePopup.open()
                    }
                }
            }

            Popup {
                id: createCuePopup

                parent: Overlay.overlay

                x: 1280
                y: 620
                width: 420
                height: 270
                padding: 5

                background: Rectangle {
                    color: "orange"
                }
                
                // Cue ID Selector
                Item {
                    id: cueIdSelector
                    height: 50
                    anchors.top: parent.top
                    anchors.topMargin: 10
                    Text{
                        id: cueIdSelectorText
                        text: "Cue Id:"
                        anchors.left: parent.left
                        anchors.leftMargin: 10
                        anchors.verticalCenter: parent.verticalCenter
                        color: "white"
                    }

                    Rectangle {
                        id: cueIdSelectorTextInputBackground
                        anchors.left: parent.left
                        anchors.leftMargin: 100
                        width: 300
                        height: 50
                        color: "white"
                        border.color: "black"
                        border.width: 1

                        TextInput {
                            id: cueIdSelectorTextInput
                            anchors.fill: parent
                            width: 300
                            height: 50
                            leftPadding: 10
                            verticalAlignment: TextInput.AlignVCenter
                            color: "black"
                            text: "1"

                            onTextChanged: {
                                cueId = text
                            }
                        }
                    }
                }

                // Cue Name Selector
                Item {
                    id: cueNameSelector
                    height: 50
                    anchors.top: cueIdSelector.bottom
                    anchors.topMargin: 10
                    Text{
                        id: cueNameSelectorText
                        text: "Cue Name:"
                        anchors.left: parent.left
                        anchors.leftMargin: 10
                        anchors.verticalCenter: parent.verticalCenter
                        color: "white"
                    }

                    Rectangle {
                        id: cueNameSelectorTextInputBackground
                        anchors.left: parent.left
                        anchors.leftMargin: 100
                        width: 300
                        height: 50
                        color: "white"
                        border.color: "black"
                        border.width: 1

                        TextInput {
                            id: cueNameSelectorTextInput
                            anchors.fill: parent
                            width: 300
                            height: 50
                            leftPadding: 10
                            verticalAlignment: TextInput.AlignVCenter
                            color: "black"
                            text: "Cue X"

                            onTextChanged: {
                                cueName = text
                            }
                        }
                    }
                }

                // Cue Group Selector
                Item {
                    id: cueGroupSelector
                    height: 50
                    anchors.top: cueNameSelector.bottom
                    anchors.topMargin: 10
                    Text{
                        id: cueGroupSelectorText
                        text: "Cue Group:"
                        anchors.left: parent.left
                        anchors.leftMargin: 10
                        anchors.verticalCenter: parent.verticalCenter
                        color: "white"
                    }

                    Rectangle {
                        id: cueGroupSelectorTextInputBackground
                        anchors.left: parent.left
                        anchors.leftMargin: 100
                        width: 300
                        height: 50
                        color: "white"
                        border.color: "black"
                        border.width: 1

                        TextInput {
                            id: cueGroudSelectorTextInput
                            anchors.fill: parent
                            width: 300
                            height: 50
                            leftPadding: 10
                            verticalAlignment: TextInput.AlignVCenter
                            color: "black"
                            text: "1"

                            onTextChanged: {
                                cueGroup = text
                            }
                        }
                    }
                }

                // Submit Button
                Item {
                    id: submitButton
                    anchors.top: cueGroupSelector.bottom
                    anchors.topMargin: 15
                    anchors.horizontalCenter: parent.horizontalCenter
                    
                    Button {
                        id: submitButtonButton
                        width: 400
                        height: 50
                        z: 2
                        anchors.horizontalCenter: parent.horizontalCenter
                        text: "Create"
                        background: Rectangle {
                            color: "green"
                            border.color: "black"
                            border.width: 1
                        }
                        onClicked: {
                            console.log("submit button clicked")
                            //create cue
                            cueListQmlPresentationModel.add_cue(cueId, cueName, cueGroup)

                            createCuePopup.close()
                        }

                    }
                }

            }

        }     
    }    
}
