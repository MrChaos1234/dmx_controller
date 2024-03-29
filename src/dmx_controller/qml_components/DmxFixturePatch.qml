import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Layouts 1.2
import QtQuick.Controls 2.15

import "../qml_pages"
import "../qml_components"
import ".."

Item {
    id: dmxFixturePatch
    width: 650
    
    property int active_fixture_global

    Rectangle {
        id: fixturePatchBackground
        anchors.fill: parent
        color: "black"
    }

    anchors {
        left: parent.left
        top: parent.top
        bottom: parent.bottom
    }

    // Header
    Rectangle {
        id: fixturePatchHeader
        anchors {
            left: parent.left
            top: parent.top
            right: parent.right
        }
        height: 50
        color: "orange"
        Text {
            id: fixturePatchHeaderText
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
            text: "Fixture Patch"
            font.family: "TW Cen MT"
            font.pixelSize: 23
            font.styleName: "Bold"
            color: "black"
        }
    }


    // Description
    Rectangle {
        id: fixturePatchDescription
        anchors {
            left: parent.left
            top: fixturePatchHeader.bottom
            right: parent.right
        }
        height: 50
        color: "black"

        Rectangle {
            id: fixturePatchDescriptionSelectBox
            height: 50
            width: 50
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.leftMargin: 4
            color: "#2a2a2a"
        }

        Rectangle {
            id: fixturePatchDescriptionIdBox
            anchors.left: fixturePatchDescriptionSelectBox.right
            anchors.leftMargin: 4
            height: 50
            width: 96
            color: "#2a2a2a"

            Text {
                id: fixturePatchDescriptionId
                anchors.centerIn: parent
                text: "ID"
                font.family: "TW Cen MT"
                font.pixelSize: 22
                color: "white"
            }
        }
        
        Rectangle {
            id: fixturePatchDescriptionTypeBox
            anchors.left: fixturePatchDescriptionIdBox.right
            anchors.leftMargin: 4
            height: 50
            width: 150
            color: "#2a2a2a"

            Text {
                id: fixturePatchDescriptionType
                anchors.centerIn: parent
                text: "TYPE"
                font.family: "TW Cen MT"
                font.pixelSize: 22
                color: "white"
            }
        }

        Rectangle {
            id: fixturePatchDescriptionNameBox
            anchors.left: fixturePatchDescriptionTypeBox.right
            anchors.leftMargin: 4
            height: 50
            width: 200
            color: "#2a2a2a"

            Text {
                id: fixturePatchDescriptionName
                anchors.centerIn: parent
                text: "NAME"
                font.family: "TW Cen MT"
                font.pixelSize: 22
                color: "white"
            }
        }

        Rectangle {
            id: fixturePatchDescriptionDmxBox
            anchors.left: fixturePatchDescriptionNameBox.right
            anchors.leftMargin: 4
            height: 50
            width: 80
            color: "#2a2a2a"

            Text {
                id: fixturePatchDescriptionDmx
                anchors.centerIn: parent
                text: "DMX"
                font.family: "TW Cen MT"
                font.pixelSize: 22
                color: "white"
            }
        }
    }


    // List
    Component {
        id: delegate
        Rectangle {
            id: wrapper
            height: 40
            color: "black"
            Rectangle {
                id: listElementSelectBox
                height: 40
                width: 50
                anchors.top: parent.top
                anchors.left: parent.left
                anchors.leftMargin: 4
                color: "#2a2a2a"
                Rectangle {
                    id: listElementSelect
                    anchors.centerIn: parent
                    width: 30
                    height: 30
                    color: display.selected ? "orange" : "white"
                }
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        dmxFixturePatchQmlPresentationModel.select(index)
                    }                        
                } 
                //display.selected
            }

            
            Rectangle {
                id: listElementIdBox
                anchors.left: listElementSelectBox.right
                anchors.leftMargin: 4
                height: 40
                width: 96
                color: "#2a2a2a"
                Text {
                    id: listElementId
                    anchors.centerIn: parent
                    text: display.identifier
                    font.family: "TW Cen MT"
                    font.pixelSize: 17
                    color: "white"
                }
            }
            Rectangle {
                id: listElementTypeBox
                anchors.left: listElementIdBox.right
                anchors.leftMargin: 4
                height: 40
                width: 150
                color: "#2a2a2a"
                Text {
                    id: listElementType
                    anchors.centerIn: parent
                    text: display.fixture_name
                    font.family: "TW Cen MT"
                    font.pixelSize: 17
                    color: "white"
                }
            }
            Rectangle {
                id: listElementNameBox
                anchors.left: listElementTypeBox.right
                anchors.leftMargin: 4
                height: 40
                width: 200
                color: "#2a2a2a"
                Text {
                    id: listElementName
                    anchors.centerIn: parent
                    text: display.fixture_display_name
                    font.family: "TW Cen MT"
                    font.pixelSize: 17
                    color: "white"
                }
            }
            Rectangle {
                id: listElementDmxBox
                anchors.left: listElementNameBox.right
                anchors.leftMargin: 4
                height: 40
                width: 80
                color: "#2a2a2a"
                Text {
                    id: listElementDmx
                    anchors.centerIn: parent
                    text: display.dmx_start_address
                    font.family: "TW Cen MT"
                    font.pixelSize: 17
                    color: "white"
                }
            }               

            
            Rectangle {
                id: listElementFixtureIconDragable
                anchors.left: listElementDmxBox.right
                anchors.leftMargin: 8
                height: 40
                width: 40
                color: "yellow"
                visible: display.in_stage_view ? false : true
                property bool moving: false

                property int active_fixture
                property int active_fixture_library_id

                MouseArea {
                    id: mouseArea
                    anchors.fill: parent

                    drag.target: listElementFixtureIconDragable

                    drag.onActiveChanged: {
                        if (mouseArea.drag.active) {
                            listView.dragItemIndex = index;
                        }
                        listElementFixtureIconDragable.Drag.drop();
                        listElementFixtureIconDragable.moving = true;
                    }
                }
                states: [
                    State {
                        when: listElementFixtureIconDragable.Drag.active
                        ParentChange {
                            target: listElementFixtureIconDragable
                            parent: root
                        }

                        AnchorChanges {
                            target: listElementFixtureIconDragable
                            anchors.horizontalCenter: undefined
                            anchors.verticalCenter: undefined
                        }
                    }
                ]


                Drag.active: mouseArea.drag.active
                Drag.hotSpot.x: listElementFixtureIconDragable.width / 2
                Drag.hotSpot.y: listElementFixtureIconDragable.height / 2

                onXChanged: {
                    console.log("X: " + x + " y: " + y)
                    if (listElementFixtureIconDragable.moving == true) {
                        anchors.leftMargin = x
                        anchors.topMargin = y 
                    }

                    // set the fixture_id to the id of the fixture that is dragged
                    active_fixture = display.identifier
                    active_fixture_library_id = display.fixture_library_id
                    active_fixture_global = display.identifier

                }
            }
        }
    }

    // Connection to detect when user dropped the fixture on the stageview
    Connections {
        target: stageViewQmlPresentationModel  
        function onAdd_fixture_to_stage_view_wish_requested(params) {
            console.log("user dropped item!")
            stageViewQmlPresentationModel.add_fixture_to_stage_view(active_fixture_global)
        }
    }

    ListView {
        id: listView
        cacheBuffer: 100
        reuseItems: true
        anchors {
            left: parent.left
            top: fixturePatchDescription.bottom
            right: parent.right
            bottom: fixturePatchFooter.top
            topMargin: 4
        }
        model: dmxFixturePatchQmlPresentationModel
        clip: true
        focus: true
        spacing: 4
        delegate: delegate
        property int dragItemIndex: -1

    }

    // Footer with buttons
    Rectangle {
        id: fixturePatchFooter
        anchors {
            left: parent.left
            right: parent.right
            bottom: parent.bottom
        }
        color: "orange"
        height: 50
        width: parent.width

        GridLayout {
            anchors.fill: parent
            height: 50
            width: parent.width
            columns: 3

            Rectangle {
                id: fixturePatchFooterAddButton
                height: 42
                width: 42
                Layout.alignment: Qt.AlignCenter
                color: "green"
                Layout.column: 0
                border.color: "black"
                border.width: 2

                Image {
                    id: fixturePatchFooterAddButtonImage
                    anchors.centerIn: parent
                    width: 30
                    height: 30
                    source: "../res/add.png"
                }

                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        newFixtureCreationPopup.open()
                    }
                }

                Popup {
                    id: newFixtureCreationPopup

                    parent: Overlay.overlay

                    x: 190
                    y: 550
                    width: 440
                    height: 340
                    padding: 5
                    topInset: 0
                    bottomInset: 0
                    leftInset: 0
                    rightInset: 0

                    background: Rectangle {
                        color: "orange"
                        radius: 10
                    }

                    CreateNewFixture {
                        id: createNewFixture
                        anchors.fill: parent
                    }
                }
            }

            Rectangle {
                id: fixturePatchFooterRemoveButton
                Layout.alignment: Qt.AlignCenter
                height: 42
                width: 42
                color: "red"
                Layout.column: 1
                border.color: "black"
                border.width: 2

                Image {
                    id: fixturePatchFooterRemoveButtonImage
                    anchors.centerIn: parent
                    width: 30
                    height: 30
                    source: "../res/trash_can.png"
                }

                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        dmxFixturePatchQmlPresentationModel.remove_selected_fixtures()
                    }
                }
            }
        }
    }
    

}