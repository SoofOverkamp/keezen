const Colors = {
    RED: "red",
    BLUE: "blue",
    YELLOW: "yellow",
    GREEN: "green",
}

export default Colors;

export function colorToText(color) {
    switch (color) {
        case Colors.RED:
            return "Rood"
        case Colors.BLUE:
            return "Blauw"
        case Colors.YELLOW:
            return "Geel"
        case  Colors.GREEN:
            return "Groen"
    }
}