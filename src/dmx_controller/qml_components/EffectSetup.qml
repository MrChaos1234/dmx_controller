import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Layouts 1.2
import QtQuick.Controls 2.15

import "../qml_pages"
import "../qml_components"
import ".."


Rectangle {
    id: effectSetup
    width: 650
    height: 160
    color: "black"
    z: 1
    
    Component.onCompleted: {
        effectsQmlPresentationModel.update_effect_cues()
        effectSetupGridEffect1CueSelector.text = effectsQmlPresentationModel.get_effect_cues(1)
        effectSetupGridEffect2CueSelector.text = effectsQmlPresentationModel.get_effect_cues(2)
        effectSetupGridEffect3CueSelector.text = effectsQmlPresentationModel.get_effect_cues(3)
        effectSetupGridEffect4CueSelector.text = effectsQmlPresentationModel.get_effect_cues(4)
    }

    // Header
    Rectangle {
        id: effectSetupHeader
        x: 0
        y: 0
        width: 650
        height: 30
        color: "orange"
        
        Text {
            id: effectSetupHeaderText
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
            text: "Effect Setup"
            font.family: "TW Cen MT"
            font.pixelSize: 20
            font.styleName: "Bold"
            color: "black"
        }
    }

    // Effect Setup
    GridLayout {
        id: effectSetupGrid
        anchors.top: effectSetupHeader.bottom
        anchors.left: effectSetup.left
        anchors.topMargin: 10
        anchors.leftMargin: 10
        width: 630
        height: 140
        columns: 4
        rows: 1

        Rectangle {
            id: effectSetupGridEffect1
            property bool saving_possible: false
            Layout.column: 0
            Layout.fillHeight: true
            width: 150
            color: "#2b2b2b"
            

            Text {
                id: effectSetupGridEffect1Text
                anchors.fill: parent
                anchors.margins: 2
                anchors.topMargin: 10
                text: "Effect 1"
                font.family: "TW Cen MT"
                font.pixelSize: 20
                color: "white"
                horizontalAlignment: Text.AlignHCenter          
            }

            // Cue Selector
            Rectangle {
                id: effectSetupGridEffect1CueSelectorBackground
                anchors.left: parent.left
                anchors.leftMargin: 10
                anchors.top: parent.top
                anchors.topMargin: 45
                width: 130
                height: 30
                color: "white"
                border.color: "black"
                border.width: 2

                TextInput {
                    id: effectSetupGridEffect1CueSelector
                    anchors.fill: parent

                    color: "black"
                    text: "0.0.0.0"
                    font.family: "TW Cen MT"
                    font.pixelSize: 17

                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                    

                    onTextChanged: {
                        effectSetupGridEffect1.saving_possible = effectsQmlPresentationModel.set_effect_cues(1, effectSetupGridEffect1CueSelector.text)
                    }
                }
            }

            // Submit Button
            Button {
                id: effectSetupGridEffect1SubmitButton
                width: 130
                height: 40
                anchors.left: parent.left
                anchors.leftMargin: 10
                anchors.top: parent.top
                anchors.topMargin: 90

                text: "Save"

                background: Rectangle {
                    color: "green"
                    border.color: "black"
                    border.width: 1
                }

                onClicked: {
                }

            }
        }

        Rectangle {
            id: effectSetupGridEffect2
            Layout.column: 1
            Layout.fillHeight: true
            width: 150
            color: "#2b2b2b"
            
            property bool saving_possible: false

            Text {
                id: effectSetupGridEffect2Text
                anchors.fill: parent
                anchors.margins: 2
                anchors.topMargin: 10
                text: "Effect 2"
                font.family: "TW Cen MT"
                font.pixelSize: 20
                color: "white"
                horizontalAlignment: Text.AlignHCenter
                
            }

            // Cue Selector
            Rectangle {
                id: effectSetupGridEffect2CueSelectorBackground
                anchors.left: parent.left
                anchors.leftMargin: 10
                anchors.top: parent.top
                anchors.topMargin: 45
                width: 130
                height: 30
                color: "white"
                border.color: "black"
                border.width: 2

                TextInput {
                    id: effectSetupGridEffect2CueSelector
                    anchors.fill: parent

                    color: "black"
                    text: "0.0.0.0"
                    font.family: "TW Cen MT"
                    font.pixelSize: 17

                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                    

                    onTextChanged: {
                        effectSetupGridEffect2.saving_possible = effectsQmlPresentationModel.set_effect_cues(2, effectSetupGridEffect2CueSelector.text)
                    }
                }
            }

            // Submit Button
            Button {
                id: effectSetupGridEffect2SubmitButton
                width: 130
                height: 40
                anchors.left: parent.left
                anchors.leftMargin: 10
                anchors.top: parent.top
                anchors.topMargin: 90

                text: "Save"

                background: Rectangle {
                    color: "green"
                    border.color: "black"
                    border.width: 1
                }

                onClicked: {
                }

            }
        }

        Rectangle {
            id: effectSetupGridEffect3
            Layout.column: 2
            Layout.fillHeight: true
            width: 150
            color: "#2b2b2b"
            
            property bool saving_possible: false

            Text {
                id: effectSetupGridEffect3Text
                anchors.fill: parent
                anchors.margins: 2
                anchors.topMargin: 10
                text: "Effect 3"
                font.family: "TW Cen MT"
                font.pixelSize: 20
                color: "white"
                horizontalAlignment: Text.AlignHCenter   
                
            }
            // Cue Selector
            Rectangle {
                id: effectSetupGridEffect3CueSelectorBackground
                anchors.left: parent.left
                anchors.leftMargin: 10
                anchors.top: parent.top
                anchors.topMargin: 45
                width: 130
                height: 30
                color: "white"
                border.color: "black"
                border.width: 2

                TextInput {
                    id: effectSetupGridEffect3CueSelector
                    anchors.fill: parent

                    color: "black"
                    text: "0.0.0.0"
                    font.family: "TW Cen MT"
                    font.pixelSize: 17

                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                    

                    onTextChanged: {
                        effectSetupGridEffect3.saving_possible = effectsQmlPresentationModel.set_effect_cues(3, effectSetupGridEffect3CueSelector.text)
                    }
                }
            }

            // Submit Button
            Button {
                id: effectSetupGridEffect3SubmitButton
                width: 130
                height: 40
                anchors.left: parent.left
                anchors.leftMargin: 10
                anchors.top: parent.top
                anchors.topMargin: 90

                text: "Save"

                background: Rectangle {
                    color: "green"
                    border.color: "black"
                    border.width: 1
                }

                onClicked: {
                }

            }
        }

        Rectangle {
            id: effectSetupGridEffect4
            Layout.column: 3
            Layout.fillHeight: true
            width: 150

            color: "#2b2b2b"
            
            property bool saving_possible: false

            Text {
                id: effectSetupGridEffect4Text
                anchors.fill: parent
                anchors.margins: 2
                anchors.topMargin: 10
                text: "Effect 4"
                font.family: "TW Cen MT"
                font.pixelSize: 20      
                color: "white"
                horizontalAlignment: Text.AlignHCenter
                
            }
            // Cue Selector
            Rectangle {
                id: effectSetupGridEffect4CueSelectorBackground
                anchors.left: parent.left
                anchors.leftMargin: 10
                anchors.top: parent.top
                anchors.topMargin: 45
                width: 130
                height: 30
                color: "white"
                border.color: "black"
                border.width: 2

                TextInput {
                    id: effectSetupGridEffect4CueSelector
                    anchors.fill: parent

                    color: "black"
                    text: "0.0.0.0"
                    font.family: "TW Cen MT"
                    font.pixelSize: 17

                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                    

                    onTextChanged: {
                        effectSetupGridEffect4.saving_possible = effectsQmlPresentationModel.set_effect_cues(4, effectSetupGridEffect4CueSelector.text)
                    }
                }
            }

            // Submit Button
            Button {
                id: effectSetupGridEffect4SubmitButton
                width: 130
                height: 40
                anchors.left: parent.left
                anchors.leftMargin: 10
                anchors.top: parent.top
                anchors.topMargin: 90

                text: "Save"

                background: Rectangle {
                    color: "green"
                    border.color: "black"
                    border.width: 1
                }

                onClicked: {
                }

            }
        }
       
    }
}
