import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Layouts 1.2
import QtQuick.Controls 2.15

import "../qml_pages"
import "../qml_components"
import ".."

Item {
    id: faders

    Component.onCompleted: {
        faderQmlPresentationModel.setupConnection(0, "/dev/ttyUSB0")
        faderQmlPresentationModel.setFadersCount(0, "4")
        faderQmlPresentationModel.setMaxMotorStopTimeoutCounter(0, 5)
    }

    Rectangle {
        id: itemArea
        color: "black"
        anchors.fill: parent
        width: 400
        height: 105

        // Top Row Fixture Name and Color
        Row {
            id: topRow
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            height: 20
        }

        // Fader Row
        Item {
            id: faderRow
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.top: topRow.bottom

            height: 105     

            Fader {
                id: fader0
                anchors.left: parent.left
                anchors.leftMargin: 2
                faderIndex: 0
                position: faderQmlPresentationModel.faderPosition0
                setValue: 200
                onSetPositionSetValue: (positionSetValue)=> {
                    faderQmlPresentationModel.setPositionSetValue(0, positionSetValue)
                }
            }
            Fader {
                id: fader1
                anchors.left: fader0.right
                anchors.leftMargin: 2
                faderIndex: 1
                position: faderQmlPresentationModel.faderPosition1
                setValue: 300
                onSetPositionSetValue: (positionSetValue)=> {
                    faderQmlPresentationModel.setPositionSetValue(1, positionSetValue)
                }
            }
            Fader {
                id: fader2
                anchors.left: fader1.right
                anchors.leftMargin: 2
                faderIndex: 2
                position: faderQmlPresentationModel.faderPosition2
                setValue: 400
                onSetPositionSetValue: (positionSetValue)=> {
                    faderQmlPresentationModel.setPositionSetValue(2, positionSetValue)
                }
            }
            Fader {
                id: fader3
                anchors.left: fader2.right
                anchors.leftMargin: 2
                faderIndex: 3
                position: faderQmlPresentationModel.faderPosition3
                setValue: 500
                onSetPositionSetValue: (positionSetValue)=> {
                    faderQmlPresentationModel.setPositionSetValue(3, positionSetValue)
                }
            }    
        }

    }
}
