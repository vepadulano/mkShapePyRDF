template
    <typename container>
    float Alt(container c, int index, float alt){
        if (index < c.size()) {
            return c[index];
        }
        else{
            return alt;
        }
    }