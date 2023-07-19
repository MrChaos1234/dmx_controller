import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Layouts 1.2
import QtQuick.Controls 2.15

import "../qml_pages"
import "../qml_components"
import ".."

Item {
    id: fader
    width: 90
    height: 105

    property int faderIndex: 0
    property int position: 1023
    property int setValue: 200
    property int positionToShow: position

    signal setPositionSetValue(positionSetValue: int)


    Connections {
        target: faderQmlPresentationModel
        function onUpdate_fader_info() {
            fader.update_fader_info()
        }
    }
    function update_fader_info() {
        faderPurposeText.text = faderQmlPresentationModel.get_channel_name(faderIndex)
        faderPurposeSymbol.source = faderQmlPresentationModel.get_channel_symbol(faderIndex)
    }
    
    Component.onCompleted: {
        update_fader_info()
    }


    Item {
        id: faderArea
        anchors.fill: parent

        Rectangle {
            id: itemArea
            color: "#2a2a2a"
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 10
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            
            // Text {
            //     anchors.centerIn: parent
            //     color: "white"
            //     text: positionToShow
            // }

            Text {
                id: faderPurposeText
                anchors.top: parent.top
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.topMargin: 8
                width: parent.width
                color: "white"
                text: ""
                font.family: "Tw Cen MT"
                font.pixelSize: 10
                wrapMode: Text.Wrap
                horizontalAlignment: Text.AlignHCenter
            }

            Image {
                id: faderPurposeSymbol
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 20
                anchors.horizontalCenter: parent.horizontalCenter
                width: 30
                height: 30
                source: "../res/empty.png"
            }
        }

        Rectangle {
            id: valueVisual
            anchors.bottom: parent.bottom
            anchors.left: parent.left
            anchors.right: parent.right
            color: Qt.rgba(255, 255, 255, 0.2)
            height: Math.round(position / 2.4)
        }
    }


    Item {
        id: flashButtonArea
        anchors.fill: parent
        
        Rectangle {
            id: flashButtonIndicator
            anchors.bottom: parent.bottom
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.leftMargin: 1
            anchors.bottomMargin: 2
            height: 8
            color: "red"
        }

    }
    
    

}