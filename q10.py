import SciServer.CasJobs as cj
import time

TOP_QUERY = 'SELECT TOP 200 * FROM censusData WHERE county is not null ORDER BY Popdensity DESC'
BOTTOM_QUERY = 'SELECT TOP 200 * FROM censusData WHERE county is not null ORDER BY Popdensity ASC'
ALL_QUERY = 'SELECT * FROM censusData WHERE county is not null'

TOP_200_COUNTIES = '(SELECT TOP 200 county FROM censusData WHERE county is not null ORDER BY Popdensity DESC)'
BOTTOM_200_COUNTIES = '(SELECT TOP 200 county FROM censusData WHERE county is not null ORDER BY Popdensity ASC)'


def getTop200():
    return cj.executeQuery(TOP_QUERY, "COVIDNYT")


def getBottom200():
    return cj.executeQuery(BOTTOM_QUERY, "COVIDNYT")


def allCounties():
    return cj.executeQuery(ALL_QUERY, "COVIDNYT")


top200 = getTop200()
bottom200 = getBottom200()
allCounties = allCounties()


print(top200['Popdensity'])

print(bottom200['Popdensity'])

top200Pop = np.sum(top200['Population'])
bottom200Pop = np.sum(bottom200['Population'])

totalPop = np.sum(allCounties['Population'])

print("\nTop 200 total population: " + str(top200Pop))
print("\nBottom 200 total population: " + str(bottom200Pop))
print("\nTotal population: " + str(totalPop))

##############


def gTop():
    sql = """
    select date, sum(cases) cases, sum(deaths) deaths
    from StatsC
    where fips in (select top 200 fips from censusData order by popdensity desc)
    group by date
    order by date
    """
    return cj.executeQuery(sql, "COVIDNYT")


def gBot():
    sql = """
    select date, sum(cases) cases, sum(deaths) deaths
    from StatsC
    where fips in (select top 200 fips from censusData order by popdensity asc)
    group by date
    order by date
    """
    return cj.executeQuery(sql, "COVIDNYT")


top = gTop()
print(top)

bottom = gBot()
print(bottom)

maxCasesT = np.argmax(top['cases'])
maxDeathsT = np.argmax(top['deaths'])
maxCasesB = np.argmax(bottom['cases'])
maxDeathsB = np.argmax(bottom['deaths'])

print(" Top 200 max cases & deaths: ")
print(top.iloc[maxCasesT])
print(top.iloc[maxDeaths]['deaths'])

print("Bottom 200 max cases & deaths: ")
print(bottom.iloc[maxCasesB])
print(bottom.iloc[maxDeathsB]['deaths’])


###########


normTopCases = 1e5 * top.iloc[maxCasesT]['cases'] / top200Pop
normTopDeaths = 1e5 * top.iloc[maxDeathsT]['deaths'] / top200Pop

normBotCases = 1e5 * bottom.iloc[maxCasesB]['cases'] / bottom200Pop
normBotDeaths = 1e5 * bottom.iloc[maxDeathsB]['deaths'] / bottom200Pop

print("Top max (cases, deaths) normalized: " +
      str((int(normTopCases), int(normalizedTopDeaths))))
print("Bottom max (cases,deaths) normalized: " + str((int(normBotCases), int(normalizedBottomDeaths))


stdTopCases=np.std(top['cases'])
stdTopDeaths=np.std(top['deaths'])

stdBottomCases=np.std(bottom['cases'])
stdBottomDeaths=np.std(bottom['deaths'])

tCases=np.abs(normTopCases - normBotCases) /
              np.sqrt((stdTopCases**2 + stdBottomCases**2))
tDeaths=np.abs(normTopDeaths - normBotDeaths) /
               np.sqrt((stdTopDeaths**2 + stdBottomDeaths**2))

print("\nT-tests for cases and deaths in top 200 vs. bottom 200 counties")
print(tCases)
print(tDeaths)
