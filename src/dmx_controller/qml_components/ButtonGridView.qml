import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Layouts 1.2
import QtQuick.Controls 2.15

import "../qml_pages"
import "../qml_components"
import ".."


Item {
    id: butonGridView
    
    Connections {
        target: cueListQmlPresentationModel  
    }

    
    Timer {
        id: visualizeKeyPressedTimer
        interval: 500
        onTriggered: keyPressedDisplay.color = "white"
    }

    Timer {
        id: visualizeKeyReleasedTimer
        interval: 500
        onTriggered: keyReleasedDisplay.color = "white"
    }

    // Header
    Rectangle {
        id: butonGridViewHeader
        x: 5
        y: 0
        width: 700
        height: 30
        color: "orange"
        
        Text {
            id: butonGridViewHeaderText
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
            text: "X Buttons"
            font.family: "TW Cen MT"
            font.pixelSize: 20
            font.styleName: "Bold"
            color: "black"
        }
    }

    Item {
        id: wrapper
        width: 700
        height: 140
        x: 5
        y: 30

        Rectangle {
            id: view
            anchors.fill: parent
            color: "black"
            
            // for debugging
            // ButtonGridViewItemCue {
            //     id: buttonGridViewItemCue
            //     x: 0
            //     y: 0
            //     width: 70
            //     height: 70
            //     tile_id: 0
            //     row: 0
            //     column: 0
            // }

            Component.onCompleted: {
                let tile_id = 0
                let cue_id = 0
                var cue_name = ""
                var visibility = false
                var cue_list = cueListQmlPresentationModel.get_cue_list()

                for (let collumn = 0; collumn <= 1; collumn++) {
                    for (let row = 0; row <= 9; row++) {
                        // Check if tile is assigned to a cue
                        if (cueListQmlPresentationModel.find_tile_cue_relation(tile_id) != "None") {
                            cue_id = cueListQmlPresentationModel.find_tile_cue_relation(tile_id)
                            for (let i = 0; i < cue_list.length; i++) {
                                if (cue_list[i]["id"] == cue_id) {
                                    cue_name = cue_list[i]["cue_name"]
                                }
                            }
                            // if yes, set visibility to true and disable mouse area to activate the cue view
                            visibility = true
                        }

                        // create the tile
                        var component
                        var fixedFixtureItem
                        component = Qt.createComponent("ButtonGridViewItemCue.qml")
                        fixedFixtureItem = component.createObject(view)
                        // set tile properties
                        fixedFixtureItem.x = row * 70
                        fixedFixtureItem.y = collumn * 70
                        fixedFixtureItem.tile_id = tile_id
                        fixedFixtureItem.row = row
                        fixedFixtureItem.column = collumn
                        fixedFixtureItem.cue_id_text = cue_id
                        fixedFixtureItem.cue_name_text = cue_name
                        fixedFixtureItem.cue_view_visible = visibility
                        fixedFixtureItem.cue_list = cue_list
                        tile_id++

                        // Reset variables
                        cue_id = 0
                        cue_name = ""
                        visibility = false
                    }
                }
            }
                
        }

        Rectangle {
            id: toggleEditModeButton
            x: -100
            y: 200
            width: 80
            height: 80
            color: "orange"
            property bool edit_mode: false

            MouseArea {
                anchors.fill: parent
                onClicked: {
                    if (toggleEditModeButton.edit_mode == true) {
                        toggleEditModeButton.edit_mode = false
                        cueListQmlPresentationModel.set_button_grid_edit_mode(false)

                        toggleEditModeButton.border.width = 0
                    } else {
                        toggleEditModeButton.edit_mode = true
                        cueListQmlPresentationModel.set_button_grid_edit_mode(true)

                        toggleEditModeButton.border.color = "red"
                        toggleEditModeButton.border.width = 5
                    }
                    
                }
            }

            Text {
                id: toggleEditModeButtonText
                anchors.verticalCenter: parent.verticalCenter
                anchors.horizontalCenter: parent.horizontalCenter
                text: "Toggle Edit Mode"
                font.family: "TW Cen MT"
                font.pixelSize: 12
                color: "black"
                width: parent.width
                wrapMode: Text.Wrap
                horizontalAlignment: Text.AlignHCenter
            }


        }

        Rectangle {
            id: toggleReactionModeButton1
            x: -95
            y: 1
            width: 68
            height: 68
            color: "orange"
            property bool reaction_mode_1: false

            MouseArea {
                anchors.fill: parent
                onClicked: {
                    if (toggleReactionModeButton1.reaction_mode_1 == true) {
                        toggleReactionModeButton1.reaction_mode_1 = false
                        toggleReactionModeButton1.border.width = 0
                        cueListQmlPresentationModel.set_button_grid_reaction_mode_1(false)
                    } else {
                        toggleReactionModeButton1.reaction_mode_1 = true
                        toggleReactionModeButton1.border.color = "red"
                        toggleReactionModeButton1.border.width = 5
                        cueListQmlPresentationModel.set_button_grid_reaction_mode_1(true)
                    }
                    
                }
            }

            Text {
                id: toggleReactionModeButton1Text
                anchors.verticalCenter: parent.verticalCenter
                anchors.horizontalCenter: parent.horizontalCenter
                text: "Toggle Reaction Mode"
                font.family: "TW Cen MT"
                font.pixelSize: 12
                color: "black"
                width: parent.width
                wrapMode: Text.Wrap
                horizontalAlignment: Text.AlignHCenter
            }


        }

        Rectangle {
            id: toggleReactionModeButton2
            x: -95
            y: 71
            width: 68
            height: 68
            color: "orange"
            property bool reaction_mode_2: false

            MouseArea {
                anchors.fill: parent
                onClicked: {
                    if (toggleReactionModeButton2.reaction_mode_2 == true) {
                        toggleReactionModeButton2.reaction_mode_2 = false
                        toggleReactionModeButton2.border.width = 0
                        cueListQmlPresentationModel.set_button_grid_reaction_mode_2(false)
                    } else {
                        toggleReactionModeButton2.reaction_mode_2 = true
                        toggleReactionModeButton2.border.color = "red"
                        toggleReactionModeButton2.border.width = 5
                        cueListQmlPresentationModel.set_button_grid_reaction_mode_2(true)
                    }
                    
                }
            }

            Text {
                id: toggleReactionModeButton2Text
                anchors.verticalCenter: parent.verticalCenter
                anchors.horizontalCenter: parent.horizontalCenter
                text: "Toggle Reaction Mode"
                font.family: "TW Cen MT"
                font.pixelSize: 12
                color: "black"
                width: parent.width
                wrapMode: Text.Wrap
                horizontalAlignment: Text.AlignHCenter
            }


        }
    }
}