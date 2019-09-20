#ifndef HEADERS_HH
#define HEADERS_HH

using namespace ROOT::VecOps;

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

RVec<double> LogVec(RVec<double> vec){
    RVec<double> out; 
    for(auto const & el : vec){
        out.push_back(TMath::Log(el));
    }
    return out;
}

#endif
