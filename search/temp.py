st = Stack()
    st2 = Stack()
    path = []
    parent = {}
    visited = {}
    opposite = {'East':'West', 'West':'East', 'North':'South', 'South':'North'}
    st.push((problem.getStartState(), '', 0))
    visited = {problem.getStartState():1}
    while(st.isEmpty() == False):
        top = st.pop()
        st2.push(top)
        nbrs = problem.getSuccessors(top[0])
        count = 0
        if top[1] != '':
            path.append(top[1])
            print top, top[1]
        for nxt in nbrs:
            if nxt[0] not in visited:
                st.push(nxt)
                visited[nxt[0]] = 1
                parent[nxt] = top
                count += 1
        if count == 0:
            if(st.isEmpty() == True):
                while(st2.isEmpty() == False):
                    curr = st2.pop()
                    if(curr[1] == ''):
                        break;
                    path.append(opposite[curr[1]])
                break
            toreach = st.pop()
            st.push(toreach)
            flag = 1
            while True:
                if(st2.isEmpty() == False):
                    curr = st2.pop()
                else:
                    break
                nbrs = problem.getSuccessors(curr[0])
                for nxt in nbrs:
                    if nxt == toreach:
                        flag = 0
                        break
                if flag == 1:
                    path.append(opposite[curr[1]])
                    print curr, opposite[curr[1]]
                else:
                    break
    print path
    return path