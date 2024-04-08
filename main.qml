import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Controls.Fusion
import QtQuick.Layouts

Window {
    id: app
    width: 1024
    height: 768
    visible: true

    title: "Worker Checkbox"

    function timerOff(){
        but_timer.checked = false
        internal.autoUpdater(false)
    }


    QtObject {
        id: internal

        function tokenTest(){
            var token = base.config_getToken()
            console.log(token)
            if (token !== ""){
                token_check.text = "OK"
                token_check.color = "#008000"

                productUpdate()

            } else {
                token_check.text = "FAIL"
                token_check.color = "#990000"

                if (stackView.depth > 0){
                    stackView.pop()
                }
                config.load()
                stackView.push(config)
            }
        }

        function productUpdate(){
            tGoods.start()
        }

        function updateNova(){
            tNova.start()
        }

        function autoUpdater(v){
            if (v){
                but_timer.text = "AUTO ON"
                updater.running = true
            } else {
                but_timer.text = "AUTO OFF"
                updater.running = false
            }
        }

    }

    Connections {
        target: tGoods

        function onStarted(){
            progressProductBar.visible = true
            productValueProgress.visible = false
        }

        function onWorking(val){
            progressProductBar.value = val
        }

        function onFinished(){
            progressProductBar.visible = false
            progressProductBar.value = 0
            product_check.text = "OK"
            product_check.color = "#008000"

            internal.updateNova()
        }

        function onFail(message){
            progressProductBar.visible = false
            progressProductBar.value = 0
            productValueProgress.text = message
            product_check.text = "FAIL"
            product_check.color = "#990000"
        }
    }

    Connections {
        target: tNova
        function onStarted(){
            progressNovaBar.visible = true
        }
        function onWorking(val){
            progressNovaBar.value = val

        }
        function onFinished(){
            progressNovaBar.visible = false
            nova_check.text = "OK"
            nova_check.color = "#008000"
        }
    }



    Rectangle {
        id: bg
        color: "#ffffff"
        anchors.fill: parent
        anchors.margins: 15

        ColumnLayout {
            anchors.fill: parent

            RowLayout {
                id: menu
                Layout.minimumHeight: 35
                Layout.maximumHeight: 35
                Layout.fillWidth: true

                Button {
                    id: button
                    text: qsTr("Налаштування")
                    Layout.fillHeight: true
                    Layout.minimumWidth: implicitWidth
                    Layout.maximumWidth: implicitWidth

                    onClicked: {
                        timerOff()

                        if (stackView.depth > 0){
                            stackView.pop()
                        }
                        config.load()
                        stackView.push(config)


                    }
                }

                Button {
                    id: button1
                    Layout.fillHeight: true
                    Layout.minimumWidth: implicitWidth
                    Layout.maximumWidth: implicitWidth
                    text: qsTr("Товари в Checkbox")

                    onClicked: {
                        timerOff()

                        if (stackView.depth > 0){
                            stackView.pop()
                        }
                        product.load()
                        stackView.push(product)
                    }
                }
                Button {
                    id: but_order
                    Layout.fillHeight: true
                    Layout.minimumWidth: implicitWidth
                    Layout.maximumWidth: implicitWidth
                    text: qsTr("Обробка файлів")

                    onClicked: {
                        timerOff()

                        if (stackView.depth > 0){
                            stackView.pop()
                        }
                        stackView.push(orders)
                    }
                }

                Button {
                    id: button3
                    Layout.fillHeight: true
                    Layout.minimumWidth: implicitWidth
                    Layout.maximumWidth: implicitWidth
                    text: qsTr("Замовлення з ТТН")

                    onClicked: {
                        timerOff()

                        if (stackView.depth > 0){
                            stackView.pop()
                        }
                        ttn.load()
                        stackView.push(ttn)
                    }
                }

                Item {
                    id: item1
                    Layout.fillWidth: true
                }

                Button {
                    id: but_timer
                    Layout.fillHeight: true
                    Layout.minimumWidth: 120
                    Layout.maximumWidth: 120
                    text: qsTr("AUTO OFF")

                    checkable: true
                    checked: false

                    onClicked: internal.autoUpdater(checked)
                }
            }

            StackView {
                id: stackView
                initialItem: pane
                Layout.fillHeight: true
                Layout.fillWidth: true
            }
        }
    }

    Pane {
        id: pane

        ColumnLayout {
            anchors.fill: parent
            spacing: 5

            Item {
                Layout.fillWidth: true
                Layout.minimumHeight: app.height / 2
                Layout.maximumHeight: app.height / 2

                Label {
                    id: l_title
                    anchors.centerIn: parent

                    text: "Worker Checkbox"
                    font.pointSize: 19
                }
            }
            Item {
                Layout.fillHeight: true
            }

            RowLayout {
                Layout.fillWidth: true
                Layout.minimumHeight: 30
                Layout.maximumHeight: 30

                spacing: 25
                Label {
                    Layout.minimumWidth: implicitWidth
                    Layout.maximumWidth: implicitWidth
                    Layout.fillHeight: true

                    text: "Checkbox Token test:"
                    font.pointSize: 11

                }

                Label {
                    id: token_check
                    Layout.minimumWidth: implicitWidth
                    Layout.maximumWidth: implicitWidth
                    Layout.fillHeight: true
                    font.pointSize: 9

                }
                Item {
                    Layout.fillWidth: true
                }
            }

            RowLayout {
                id: updProduct
                Layout.fillWidth: true
                Layout.minimumHeight: 30
                Layout.maximumHeight: 30

                spacing: 25

                Label {
                    Layout.minimumWidth: implicitWidth
                    Layout.maximumWidth: implicitWidth
                    Layout.fillHeight: true

                    text: "Product update:"
                    font.pointSize: 11

                 }
                ProgressBar {
                    id: progressProductBar

                    Layout.minimumWidth: 300
                    Layout.maximumWidth: 300
                    Layout.minimumHeight: 5
                    Layout.maximumHeight: 5

                    visible: false
                    value: 0
                }
                Label {
                    id: productValueProgress
                    Layout.minimumWidth: implicitWidth
                    Layout.maximumWidth: implicitWidth
                    Layout.fillHeight: true
                    font.pointSize: 9
                }

                Label {
                    id: product_check
                    Layout.minimumWidth: implicitWidth
                    Layout.maximumWidth: implicitWidth
                    Layout.fillHeight: true
                    font.pointSize: 9

                }
                Item {
                    Layout.fillWidth: true
                }
            }
            RowLayout {
                id: updNova
                Layout.fillWidth: true
                Layout.minimumHeight: 30
                Layout.maximumHeight: 30

                spacing: 25

                Label {
                    Layout.minimumWidth: implicitWidth
                    Layout.maximumWidth: implicitWidth
                    Layout.fillHeight: true

                    text: "NovaPoshta update:"
                    font.pointSize: 11

                 }
                ProgressBar {
                    id: progressNovaBar

                    Layout.minimumWidth: 300
                    Layout.maximumWidth: 300
                    Layout.minimumHeight: 5
                    Layout.maximumHeight: 5

                    visible: false
                    value: 0
                }

                Label {
                    id: nova_check
                    Layout.minimumWidth: implicitWidth
                    Layout.maximumWidth: implicitWidth
                    Layout.fillHeight: true
                    font.pointSize: 9

                }
                Item {
                    Layout.fillWidth: true
                }
            }
        }
    }

    Setting {
        id: config
        visible: false
    }

    Products {
        id: product
        visible: false
    }

    Orders {
        id: orders
        visible: false
    }

    TTN {
        id: ttn
        visible: false
    }

    Timer {
        id: starter
        interval: 2000;
        running: true;
        repeat: false
        onTriggered: internal.tokenTest()
     }

    Timer {
        id: updater
        interval: 30000
        running: false
        repeat: true
        onTriggered: internal.updateNova()
    }


    property int _x: 0
    property int _y: 0

    onXChanged: {
        setGeometry(app.x, app.y, app.width, app.height)
    }

    onYChanged: {
        setGeometry(app.x, app.y, app.width, app.height)
    }

    onWidthChanged: {
        if (_x === 0){
            setGeometry(app.x + 1, app.y, app.width, app.height)
            _x = 1
        } else {
            setGeometry(app.x - 1, app.y, app.width, app.height)
            _x = 0
        }
    }

    onHeightChanged: {
        if (_y === 0){
            setGeometry(app.x, app.y + 1, app.width, app.height)
            _y = 1
        } else {
            setGeometry(app.x, app.y - 1, app.width, app.height)
            _y = 0
        }
    }
}
