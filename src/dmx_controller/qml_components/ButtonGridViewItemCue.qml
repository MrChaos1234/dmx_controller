import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15

import "../qml_pages"
import "../qml_components"
import ".."


Rectangle {
    id: buttonGridViewItemCue
    width: 70
    height: 70
    color: "black"
    z: 1

    // variables set from outside
    property int tile_id: 0
    property int row: 0
    property int column: 0
    property int cue_id_text: 0
    property string cue_name_text: ""
    property bool cue_view_visible: false
    property bool mouse_area_enabled: true
    property var cue_list: []

    // internal!
    property int cue_id: 0  // only set correct right after the relation is created
    property string cue_name: ""
    property bool reaction_mode: false
    property bool pressed: false


    Connections {
        target: cueListQmlPresentationModel
        function onUpdate_currentCueName(name) {
            console.log("updating cue name")
            cueSelectorTextName.text = name
            cue_name = name
        }
        function onUpdate_currentCueId(id) {
            cueSelectorTextId.text = id
            cue_id = id
        }
    }

    
    MouseArea {
        id: mouseAreaAddCue
        anchors.fill: parent
        
        enabled: mouse_area_enabled

        onPressed: {
            // only working when button grid is in edit mode
            if(cueListQmlPresentationModel.get_button_grid_edit_mode() == true) {
                // select which cue this button should represent
                selectCuePopup.open()
            }
            else {
                
                // this part is executet when not in edit mode

                if(tile_id <= 9){
                    buttonGridViewItemCue.reaction_mode = cueListQmlPresentationModel.get_button_grid_reaction_mode_1()
                }
                else {
                    buttonGridViewItemCue.reaction_mode = cueListQmlPresentationModel.get_button_grid_reaction_mode_2()
                }

                if(buttonGridViewItemCue.reaction_mode == true) {
                    // if in reaction mode, the cue has to be pressed to start and pressed again to be cleared
                    if(cueListQmlPresentationModel.get_button_state(tile_id) == false){
                        // if the cue was created in this session, cue_id has to be used.
                        // if it was created in the last session, cue_text_id has to be used
                        var id = 0
                        if(cue_id_text != 0) {
                            id = cue_id_text
                        }
                        else {
                            id = cue_id
                        }
                        artnetOutputQmlPresentationModel.execute_cue(id) // execute the cue

                        cueListQmlPresentationModel.set_button_state(tile_id, true)
                    }
                    else {
                        // if the cue was created in this session, cue_id has to be used.
                        // if it was created in the last session, cue_text_id has to be used
                        var id = 0
                        if(cue_id_text != 0) {
                            id = cue_id_text
                        }
                        else {
                            id = cue_id
                        }
                        artnetOutputQmlPresentationModel.clear_cue(id) // clear the cue

                        cueListQmlPresentationModel.set_button_state(tile_id, false)
                    }
                }
                else {
                    // if not in reaction mode, the cue is executed when the button is pressed and cleared when released
                    // if the cue was created in this session, cue_id has to be used.
                    // if it was created in the last session, cue_text_id has to be used
                    var id = 0
                        if(cue_id_text != 0) {
                            id = cue_id_text
                        }
                        else {
                            id = cue_id
                        }
                    artnetOutputQmlPresentationModel.execute_cue(id) // execute the cue
                }
            }

        }

        onReleased: {
            // only working when button grid is not in edit mode
            if(cueListQmlPresentationModel.get_button_grid_edit_mode() == true) {
                // do nothing
            }
            else {
                // this part is executet when not in edit mode
                if(tile_id <= 9){
                    buttonGridViewItemCue.reaction_mode = cueListQmlPresentationModel.get_button_grid_reaction_mode_1()
                }
                else {
                    buttonGridViewItemCue.reaction_mode = cueListQmlPresentationModel.get_button_grid_reaction_mode_2()
                }
                    if(buttonGridViewItemCue.reaction_mode == true) {
                        // if in reaction mode, the cue has to be pressed to start and pressed again to be cleared
                        console.log("reaction mode")
                    }
                    else {
                        // if not in reaction mode, the cue is executed when the button is pressed and cleared when released
                        var id = 0
                        if(cue_id_text != 0) {
                            id = cue_id_text
                        }
                        else {
                            id = cue_id
                        }
                        artnetOutputQmlPresentationModel.clear_cue(id) // clear the cue
                    }

            }
        }
    } 
    
    // Text containing the Tile Id
    Rectangle {
        id: tileIdBackground
        anchors.centerIn: parent
        color: "#2b2b2b"
        width: 66
        height: 66
        z: 2

        Text {
            id: tileIdText
            anchors.centerIn: parent
            text: tile_id
            font.family: "TW Cen MT"
            font.pixelSize: 10
            color: "white"
            z:3
        }
    }

    Popup {
        id: selectCuePopup

        parent: Overlay.overlay

        x: 220
        y: 160
        width: 200
        height: 200
        padding: 5

        

        background: Rectangle {
            color: "orange"
            border.color: "black"
            border.width: 2
            radius: 5
        }
        // Delete Button
        Item {
            id: deleteButton
            anchors.top: parent.top
            anchors.topMargin: 10
            anchors.horizontalCenter: parent.horizontalCenter
            height: 50
            Button {
                id: deleteButtonButton
                width: 180
                height: 50
                z: 2
                anchors.horizontalCenter: parent.horizontalCenter
                text: "Delete"
                background: Rectangle {
                    color: "red"
                    border.color: "black"
                    border.width: 1
                }
                onClicked: {
                    //console.log("submit button clicked")
                    // add cue to tile
                    cueListQmlPresentationModel.remove_tile_cue_relation(tile_id, cue_id)
                    // make the cue view invisible
                    cue_view.visible = false
                    selectCuePopup.close()
                }

            }
        }


        
        // Cue Selector
        Item {
            id: cueSelector
            height: 50
            anchors.top: deleteButton.bottom
            anchors.topMargin: 10
            anchors.left: parent.left
            anchors.leftMargin: 5
            Rectangle {
                id: cueSelectorBackground
                anchors.top: parent.top
                width: 180
                height: 50
                color: "white"
                border.color: "black"
                border.width: 1

                ComboBox {
                    id: cueSelectorComboBox
                    anchors.fill: parent
                    width: 180
                    height: 50
                    model: cueListQmlPresentationModel
                    textRole: "display"
                    delegate: delegateCueSelector
                    background: Rectangle {
                        color: "white"
                        border.color: "black"
                        border.width: 1
                    }
                    onCurrentIndexChanged: {
                        //console.log("current index changed to: " + currentIndex)
                        model.update_current_index(currentIndex)
                    }    

                    Rectangle {
                        id: cueSelectorTextBackground
                        anchors.fill: parent
                        color: "white"
                        border.color: "black"
                        border.width: 1

                        Text {
                            id: cueSelectorTextId
                            anchors.left: parent.left
                            anchors.leftMargin: 10
                            anchors.verticalCenter: parent.verticalCenter
                            text: ""
                            color: "black"
                        }

                        Text {
                            id: cueSelectorTextName
                            anchors.left: cueSelectorTextId.right
                            anchors.leftMargin: 5
                            anchors.verticalCenter: parent.verticalCenter
                            text: "Select a cue"
                            color: "black"
                        }
                    }   

                }
            }

        }
        // Delegate component of the cue selector ComboBox
        Component {
            id: delegateCueSelector
            ItemDelegate {
                id: delegateCueSelectorBackground
                width: 180
                height: 50
                background: Rectangle {
                    color: "white"
                    border.color: "black"
                    border.width: 1
                }
                contentItem: Text {
                    id: text
                    text: model.display.identifier + " " + model.display.cue_name + " " + model.display.cue_group
                    color: "black"
                }
            }
            
        }

        // Submit Button
        Item {
            id: submitButton
            anchors.top: cueSelector.bottom
            anchors.topMargin: 15
            anchors.horizontalCenter: parent.horizontalCenter
            
            Button {
                id: submitButtonButton
                width: 180
                height: 50
                z: 2
                anchors.horizontalCenter: parent.horizontalCenter
                text: "Add"
                background: Rectangle {
                    color: "green"
                    border.color: "black"
                    border.width: 1
                }
                onClicked: {
                    //console.log("submit button clicked")
                    // add cue to tile
                    console.log("cue_id: " + cue_id)
                    console.log("tile_id: " + tile_id)
                    cueListQmlPresentationModel.add_tile_cue_relation(tile_id, cue_id)
                    // make the cue view visible
                    cue_view.visible = true
                    // update cue view with the coorect cue name
                    for (let i = 0; i < cue_list.length; i++) {
                        if (cue_list[i]["id"] == cue_id) {
                            cue_name_text = cue_list[i]["cue_name"]
                        }
                    }
                    selectCuePopup.close()
                }

            }
        }

    }

    // Cue View
    Item {
        id: cue_view
        anchors.centerIn: parent
        width: 66
        height: 66

        z: 4
        visible: cue_view_visible

        Rectangle {
            id: cueViewBackground
            anchors.fill: parent
            color: "#2b2b2b"
            border.color: "yellow"
            border.width: 1

            Text {
                id: cueText
                anchors.centerIn: parent
                text: cue_name_text
                font.family: "TW Cen MT"
                font.pixelSize: 10
                color: "white"
                z:3
                width: parent.width
                wrapMode: Text.Wrap
                horizontalAlignment: Text.AlignHCenter
            }
        }
    }
}
