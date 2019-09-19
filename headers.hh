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

using namespace ROOT::VecOps;

RVec<double> Loggone(RVec<double>numeri){
    RVec<double> out; 
    for(auto const & a : numeri){
        out.push_back(TMath::Log(a));
    }
    return out;
}