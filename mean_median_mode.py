def median(theset: tuple[int, ...]):
    ordered = list(theset)
    #print(ordered)
    ordered.sort()
    #print(ordered)
    if len(ordered) % 2 == 0:
        iright = round(len(ordered)/2)
        #print(iright)
        ileft = iright - 1
        calc_mean = (ordered[iright]+ordered[ileft])/2
        return calc_mean
    else:
        calc_mean = ordered[round((len(ordered)+1)/2)-1]
        return calc_mean

def mean(theset: tuple[int, ...]):
    return sum(theset)/len(theset)

def mymode(theset: tuple[int, ...]):
    piece_counts = {}
    #print(piece_counts)
    for num in theset:
        if not str(num) in piece_counts.keys():
            #print("Putting",num,"in?")
            piece_counts[str(num)] = 1
        else:
            #print(piece_counts)
            piece_counts[str(num)] = piece_counts[str(num)] + 1
    max_appearence = max(piece_counts.values())
    print("Counts of each number:", piece_counts)
    results = tuple(filter(lambda lnum:
        piece_counts[lnum] == max_appearence, piece_counts.keys()))
    return tuple(sorted(results))

if __name__ == '__main__':
    _theeset: list[int] = [5, 5, 1, 7, 6, 8, 9, 10]
    #theeset.sort()
    _tupleeset: tuple[int, ...] = tuple(_theeset)
    print("Numbers:", _tupleeset)
    print("Mean:", mean(_tupleeset))
    print("Median:", median(_tupleeset))
    print("Mode:", mymode(_tupleeset))
    _newnumbers: tuple[int, ...] = (6,) + _tupleeset
    print("New numbers", _newnumbers)
    print("Mean:", mean(_newnumbers))
    print("Median:", median(_newnumbers))
    print("Mode:", mymode(_newnumbers))
