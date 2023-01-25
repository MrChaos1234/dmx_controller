import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Layouts 1.2
import QtQuick.Controls 2.15

import "../qml_pages"

Item {
    id: rightMenuBar
    width: 92
    anchors{
        top: parent.top
        right: parent.right
        rightMargin: 4
        bottom: parent.bottom
        bottomMargin: 121
    }

    property bool liveViewActive: true
    property bool recordViewActive: false
    property bool setupViewActive: false

    GridLayout {
        id: buttonsColumn
        anchors.fill: parent

        columns: 1
        rows: 2

        Rectangle {
            id: liveBtn
            Layout.row: 0
            Layout.column: 0
            Layout.fillWidth: true
            Layout.topMargin: 12
            implicitHeight: 96
            color: "#1b1b1b"
            border.color: liveViewActive ? "orange" : "transparent"
            border.width: 2

            Text {
                id: liveBtnText
                anchors.centerIn: parent
                color: "white"
                text: "Live"
                font.family: "TW Cen MT"
                font.pixelSize: 22
            }     

            MouseArea {
                anchors.fill: parent
                onClicked: {
                    mainLoader.source = "../qml_pages/LivePage.qml" 
                    if (rightMenuBar.liveViewActive == false) {
                        rightMenuBar.liveViewActive = true
                        rightMenuBar.recordViewActive = false
                        rightMenuBar.setupViewActive = false
                    }
                }
            }
        }

        Rectangle {
            id: recordBtn
            Layout.row: 1
            Layout.column: 0
            Layout.fillWidth: true
            Layout.topMargin: 8
            implicitHeight: 96
            color: "#1b1b1b"
            border.color: recordViewActive ? "orange" : "transparent"
            border.width: 2

            Text {
                id: recordBtnText
                anchors.centerIn: parent
                color: "white"
                text: "Record"
                font.family: "TW Cen MT"
                font.pixelSize: 22
            }     

            MouseArea {
                anchors.fill: parent
                onClicked: {
                    mainLoader.source = "../qml_pages/RecordPage.qml"
                    if (rightMenuBar.recordViewActive == false) {
                        rightMenuBar.liveViewActive = false
                        rightMenuBar.recordViewActive = true
                        rightMenuBar.setupViewActive = false
                    }
                }
            }
        }

        Rectangle {
            id: setupBtn
            Layout.row: 2
            Layout.column: 0
            Layout.fillWidth: true
            Layout.topMargin: 8
            implicitHeight: 96
            color: "#1b1b1b"
            border.color: setupViewActive ? "orange" : "transparent"
            border.width: 2

            Text {
                id: setupBtnText
                anchors.centerIn: parent
                color: "white"
                text: "Setup"
                font.family: "TW Cen MT"
                font.pixelSize: 22
            }     

            MouseArea {
                anchors.fill: parent
                onClicked: {
                    mainLoader.source = "../qml_pages/SetupPage.qml"
                    if (rightMenuBar.setupViewActive == false) {
                        rightMenuBar.liveViewActive = false
                        rightMenuBar.recordViewActive = false
                        rightMenuBar.setupViewActive = true
                    }
                }
            }
        }

        Rectangle {
            id: placeholder
            Layout.row: 3
            Layout.column: 0
            Layout.fillWidth: true
            implicitHeight: 740
            color: "white"
            opacity: 0
        }
            
    }
}
