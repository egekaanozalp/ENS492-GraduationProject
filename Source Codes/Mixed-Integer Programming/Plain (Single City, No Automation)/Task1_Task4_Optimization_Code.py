from gurobipy import GRB, Model, quicksum, LinExpr
import pandas as pd


def Output(m, city_name):  
    # Print the result:
    status_code = {1:'LOADED', 2:'OPTIMAL', 3:'INFEASIBLE', 4:'INF_OR_UNBD', 
                   5:'UNBOUNDED'}
    status = m.status
    
    file_name = city_name + "_Buyuksehir_Belediye_Sonuc.txt"
    text_file = open(file_name, "w")
    text_file.write(city_name + " Büyükşehir Belediyesi Seçilen Mahalleler\n\n")
    
    print('The optimization status is ' + status_code[status])
    if status == 2:      
        # Retrieve variables value:
        print('Optimal solution:')
        for v in m.getVars():
            if v.x != 0:
                print(str(v.varName) + " = " + str(v.x))
                text_file.write(str(v.varName) + " = " + str(v.x) + "\n")
        print('Optimal objective value: ' + str(m.objVal) + "\n")
        text_file.write("\n" + 'Optimal objective value: ' + str(m.objVal) + "\n")
        text_file.close()


# m = # of parties
# n = # of total neighborhoods
# k = # of neighborhoods to be selected
# G = # of votes for each party / # of total votes (priority coefficient)
# M = Matrix that includes all of the info about the election
def OptNeighborhoods(m_2014, m_2019, n, k, G_2014, G_2019, M_2014, M_2019, neigh_names, city_name):
    # Create the model
    model = Model('Neighborhood_Selection')
    
    # Set MIP gap absolute value
    model.setParam('MIPGapAbs', 1e-3)
    
    # Decision Variables:
    # 1 >= c_i >= 0 and c_i ∈ R. Represents the importance coefficient of the ith
    # neighborhood.
    c = model.addVars(n, vtype=GRB.CONTINUOUS, lb=0.0, ub=1.0, name=["c_"+ str(neigh_names[i]) for
                                                                     i in range(n)])
    # x_i = 1 if ith neighborhood is selected, 0 otherwise.
    x = model.addVars(n, vtype=GRB.BINARY, name=["x_"+ str(neigh_names[j]) for j in range(n)])
    
    # Objective Function:
    obj_expr = LinExpr()
    
    for j in range(m_2014):
        term1 = G_2014[j] - quicksum(c[i] * M_2014.iloc[i][j] for i in range(n))
        obj_expr += term1*term1
        
    for j in range(m_2019):
        term2 = G_2019[j] - quicksum(c[i] * M_2019.iloc[i][j] for i in range(n))
        obj_expr += term2*term2
                
        
    model.setObjective(obj_expr, GRB.MINIMIZE)
        
    # Constraints:
    # Choose at most "k" neighborhoods:
    model.addConstr(quicksum(x[i] for i in range(n)) == k)
    # If you did not select the neighborhood then its weight coefficient should be
    # zero:
    model.addConstrs(c[i] <= x[i] for i in range(n))
    # The summation of coefficients of the selected neighbors should add up to 1.
    model.addConstr(quicksum(c[i] for i in range(n)) == 1)
    
    # Optimize the model
    model.optimize()
    
    # print the LP file
    model.write('Neighborhood_Selection.lp')
    
    # print the sol file
    model.write('Neighborhood_Selection.sol')
    
    Output(model, city_name)
    
def main():
    # Create the election DataFrames:
    df_election_2014 = pd.read_excel("ADANA_2014_Percentage_Results.xlsx")
    df_election_2019 = pd.read_excel("ADANA_2019_Percentage_Results.xlsx")
    df_election_2014_2 = pd.read_excel("_Summed_Up_Results_ADANA_2014.xlsx")
    df_election_2019_2 = pd.read_excel("_Summed_Up_Results_ADANA_2019.xlsx")
    
    # Consider only the top 5 of the political parties (popularitywise).
    columns_2014 = df_election_2014[sorted(set(df_election_2014.columns[8:]))].sum().nlargest(5).index
    columns_2019 = df_election_2019[sorted(set(df_election_2019.columns[8:]))].sum().nlargest(5).index
    
    
    # Create the final version of the matrices that will be processed:
    M_2014 = df_election_2014[columns_2014].fillna(0)
    M_2019 = df_election_2019[columns_2019].fillna(0)
    M_2014_2 = df_election_2014_2[columns_2014].fillna(0)
    M_2019_2 = df_election_2019_2[columns_2019].fillna(0)
    
    
    # Adjust the neighbor names:
    neigh_names = [row["İlçe Adı"].replace(" ", "_").replace("İ", "I").
                   replace("Ö", "O").replace("Ğ", "G").replace("Ü", "U").
                   replace("Ş", "S").replace("Ç", "C") + "_" + row["Mahalle/Köy"].
                   replace(" ", "_").replace("İ", "I").replace("Ö", "O").
                   replace("Ğ", "G").replace("Ü", "U").replace("Ş", "S").
                   replace("Ç", "C") for index, row in df_election_2014.iterrows()]
    
    # Actual result of the parties:
    G_2014 = [(M_2014_2.sum()[i])/(M_2014_2.sum().sum()) for i in range(len(M_2014_2.sum()))]
    G_2019 = [(M_2019_2.sum()[i])/(M_2019_2.sum().sum()) for i in range(len(M_2019_2.sum()))]
    
    # Specify the k value:
    k = int(input("Please enter the amount of neighborhoods to be selected: "))
    
    # Specify the city name:
    city_name = "Adana"
    
    # Use the model:
    OptNeighborhoods(len(M_2014.columns), len(M_2019.columns), len(neigh_names),
                     k, G_2014, G_2019, M_2014, M_2019, neigh_names, city_name)

    
main()