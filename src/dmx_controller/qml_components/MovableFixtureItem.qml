import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15

import "../qml_pages"
import "../qml_components"
import ".."


Rectangle {
    id: movableFixtureItem
    width: 50
    height: 50
    color: "white"

    property int fixture_id: 0

    property string image_source: "../data/fixture_library/symbols/none.png"

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        drag.target: movableFixtureItem

        onReleased: {
            console.log("released fixture " + fixture_id)

            // Now update the position to the database!
            stageViewQmlPresentationModel.change_fixture_stage_view_coordinates(fixture_id, movableFixtureItem.x, movableFixtureItem.y)

            // if the coordinates are withing the deleting area, delete the fixture
            if (stageViewQmlPresentationModel.check_if_fixture_is_in_deleting_area(fixture_id, movableFixtureItem.x, movableFixtureItem.y) == true) {
                sureToDeletePopup.open()
            }
                
        }
                                    
        drag.onActiveChanged: {
            if (mouseArea.drag.active) {
                console.log("dragged fixture " + fixture_id)
            }
        }    
    } 

    // Image of the fixturetype
    Image {
        id: image
        anchors.top: parent.top
        anchors.horizontalCenter: parent.horizontalCenter
        width: 38
        height: 38
        
        source: image_source
    } 

    // Text containing the fixture id
    Text {
        id: fixtureIdText
        anchors.bottom: parent.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        text: fixture_id
        font.family: "TW Cen MT"
        font.pixelSize: 10
        color: "black"
    }

    Popup {
        id: sureToDeletePopup

        parent: Overlay.overlay

        x: 1110
        y: 370
        width: 350
        height: 100
        padding: 5

        background: Rectangle {
            color: "red"
        }
        
        Text{
            text: "Are you sure you want to delete this fixture?"
            font.family: "TW Cen MT"
            font.pixelSize: 15
            color: "black"
            anchors.horizontalCenter: parent.horizontalCenter
            y: 10
        }

        Button {
            id: yesButton
            text: "Yes"
            font.family: "TW Cen MT"
            font.pixelSize: 15
            width: 100
            x: 50
            y: 50
            onClicked: {
                stageViewQmlPresentationModel.delete_fixture_from_stage_view(fixture_id)
                sureToDeletePopup.close()
                movableFixtureItem.destroy()
                dmxFixturePatchQmlPresentationModel.update_fixture_patch()
            }
        }

        Button {
            id: noButton
            text: "No"
            font.family: "TW Cen MT"
            font.pixelSize: 15
            width: 100
            x: 180
            y: 50
            onClicked: {
                sureToDeletePopup.close()
            }
        }

    }
}
