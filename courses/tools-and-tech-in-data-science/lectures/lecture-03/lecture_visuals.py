"""Presentation figures used by the short teaching cells in Lecture 3."""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

EPA = '#176B87'
METEO = '#D66A2C'
MISSING = '#D7DDE2'


def location_chart():
    # EPA coordinate is an approximate H-8 location from exp4a_meteostat_test.py.
    lat = np.array([33.68031, 33.6167])
    lon = np.array([73.06205, 73.1])
    x = (lon - 73.05) * 111.32 * np.cos(np.radians(lat.mean()))
    y = (lat - 33.60) * 111.32
    separation = np.hypot(*(np.array([x[0]-x[1], y[0]-y[1]])))
    fig, ax = plt.subplots(figsize=(11, 6))
    ax.plot(x, y, '--', color='#8B9298', linewidth=1.5)
    ax.scatter(x, y, s=180, c=[EPA, METEO], edgecolors='white', zorder=3)
    ax.annotate('Pak-EPA: approximate H-8 area\nMonitor reported in H-8/2\n33.68031° N, 73.06205° E (approx.)',
                (x[0], y[0]), xytext=(18, -2), textcoords='offset points', va='center', fontsize=12)
    ax.annotate('Meteostat 41571: Islamabad Airport\n33.6167° N, 73.1000° E; elevation 507 m',
                (x[1], y[1]), xytext=(18, -10), textcoords='offset points', ha='left', fontsize=11)
    ax.text(5.0, 5.0, f'≈ {separation:.1f} km between plotted points\nIllustrative distance; exact EPA\nsensor coordinate unverified', fontsize=11)
    ax.annotate('N', xy=(12.5, 8.5), xytext=(12.5, 7), ha='center', fontsize=13,
                arrowprops={'arrowstyle': '-|>', 'color': '#333333'})
    ax.plot([0, 2], [.35, .35], color='#333333', linewidth=3)
    ax.text(1, .05, '2 km', ha='center')
    ax.set(xlim=(-1, 15), ylim=(-.7, 10.5), aspect='equal',
           title='Two locations: will their daily weather agree?')
    ax.set_xlabel('East–west distance (km, local coordinate sketch)')
    ax.set_ylabel('North–south distance (km)')
    ax.grid(alpha=.2)
    fig.text(.5, .015, 'Coordinate sketch, not a street map. Sources: Meteostat station metadata; research-script approximate EPA point.', ha='center', fontsize=9)
    fig.tight_layout(rect=(0,.04,1,1))
    plt.show()


def join_picture():
    fig, ax = plt.subplots(figsize=(11,4.5))
    ax.set(xlim=(0,11), ylim=(-.7,4.5)); ax.axis('off')
    ax.text(1,4,'EPA dates',color=EPA,weight='bold',fontsize=15)
    ax.text(5,4,'Meteostat dates',color=METEO,weight='bold',fontsize=15)
    ax.text(8.2,4,'LEFT JOIN result',weight='bold',fontsize=15)
    for k,day in enumerate([1,2,3,4]):
        y=3.2-k*.85
        ax.text(1,y,f'Jan {day}',fontsize=14,bbox={'boxstyle':'round,pad=.3','fc':'#E8F1F5','ec':'none'})
        ax.text(8.2,y,f'Jan {day}  |  '+('NULL weather' if day==3 else 'weather matched'),fontsize=12)
        if day!=3:
            ax.text(5,y,f'Jan {day}',fontsize=14,bbox={'boxstyle':'round,pad=.3','fc':'#FBEBDD','ec':'none'})
            ax.add_patch(FancyArrowPatch((2.2,y+.05),(4.7,y+.05),arrowstyle='->',mutation_scale=15,color='#777777'))
        else:
            ax.text(5,y,'No record',color='#777777',fontsize=13)
    ax.text(1,-.55,'4 EPA rows → 4 joined rows. Missing weather does not erase the pollution reading.',fontsize=13)
    fig.tight_layout(); plt.show()


def monthly_coverage(epa):
    fields=['epa_temperature_c','epa_humidity_pct','no2_ug_m3','so2_ug_m3','pm25_ug_m3']
    count=epa.set_index('date')[fields].resample('MS').count()
    days=count.index.days_in_month.to_numpy()
    pct=count.div(days,axis=0)*100
    fig,ax=plt.subplots(figsize=(12,3.6))
    im=ax.imshow(pct.T,aspect='auto',vmin=0,vmax=100,cmap='YlGnBu',interpolation='nearest')
    ticks=[i for i,d in enumerate(count.index) if d.month==1]
    ax.set_xticks(ticks,[str(count.index[i].year) for i in ticks])
    ax.set_yticks(range(5),['EPA temperature','EPA humidity','NO₂','SO₂','PM2.5'])
    ax.set_title('Where did the data disappear? Monthly calendar coverage')
    fig.colorbar(im,ax=ax,label='% of calendar days with a value',pad=.02)
    fig.tight_layout(); plt.show()


def match_counts(joined):
    counts=[(joined['_merge']=='both').sum(),(joined['_merge']=='left_only').sum()]
    fig,ax=plt.subplots(figsize=(9,2.8))
    ax.barh(['EPA dates'],[counts[0]],color=EPA,label='Weather matched')
    ax.barh(['EPA dates'],[counts[1]],left=[counts[0]],color=METEO,label='No weather match')
    ax.text(counts[0]/2,0,f'{counts[0]:,} matches',ha='center',va='center',color='white',fontsize=14)
    ax.annotate(f'{counts[1]} missing matches',xy=(sum(counts)-counts[1]/2,0),xytext=(1700,.37),
                arrowprops={'arrowstyle':'->'},fontsize=11)
    ax.set(xlim=(0,2650),ylim=(-.5,.7),xlabel='Number of EPA dates',title='The left join retains all 2,555 EPA dates')
    fig.tight_layout(); plt.show()


def agreement_summary(paired):
    fig,axes=plt.subplots(1,2,figsize=(11,3.5))
    for ax,epa,meteo,label,unit in zip(axes,
        ['epa_temperature_c','epa_humidity_pct'],['meteostat_temperature_c','meteostat_humidity_pct'],
        ['Temperature','Humidity'],['°C','percentage points']):
        diff=paired[meteo]-paired[epa]
        ax.axis('off');ax.set_title(label,weight='bold')
        ax.text(.05,.75,f'Correlation: {paired[epa].corr(paired[meteo]):.3f}',fontsize=19,transform=ax.transAxes)
        ax.text(.05,.49,f'Mean absolute error: {diff.abs().mean():.2f} {unit}',fontsize=13,transform=ax.transAxes)
        ax.text(.05,.25,f'Bias (Meteostat − EPA): {diff.mean():+.2f} {unit}',fontsize=12,transform=ax.transAxes)
    fig.suptitle(f'{len(paired):,} same-day pairs: tracking together is not the same as equality',fontsize=15)
    fig.tight_layout();plt.show()


def difference_histograms(paired):
    fig,axes=plt.subplots(1,2,figsize=(11,3.5))
    for ax,col,label,unit in zip(axes,['temp_difference','humidity_difference'],['Temperature','Humidity'],['°C','percentage points']):
        ax.hist(paired[col],bins=35,color=EPA,alpha=.85)
        ax.axvline(0,color='black',linestyle='--',label='Exact agreement')
        ax.axvline(paired[col].mean(),color=METEO,linewidth=2,label='Mean difference')
        ax.set(title=label,xlabel=f'Meteostat − EPA ({unit})',ylabel='Days')
    axes[1].legend(fontsize=9);fig.suptitle('How large are daily disagreements?')
    fig.tight_layout();plt.show()


def annual_errors(yearly_error):
    fig,axes=plt.subplots(1,2,figsize=(11,3.8))
    for ax,col,title in zip(axes,['temp_mae_c','humidity_mae_points'],['Temperature MAE (°C)','Humidity MAE (percentage points)']):
        ax.bar(yearly_error.index.astype(str),yearly_error[col],color=EPA)
        ax.set(title=title,xlabel='Year',ylabel='Mean absolute difference')
    fig.suptitle('Does agreement stay stable across years? Partial-year coverage differs.')
    fig.tight_layout();plt.show()


def fill_coverage(joined):
    fig,ax=plt.subplots(figsize=(9,3.5))
    count=joined.groupby('year')['temperature_source'].value_counts().unstack(fill_value=0)
    count.reindex(columns=['EPA','Meteostat','missing'],fill_value=0).plot.bar(stacked=True,ax=ax,color=[EPA,METEO,MISSING])
    ax.set(ylabel='EPA dates',title='Candidate temperature: preserve EPA, fill gaps from Meteostat',xlabel='Year',ylim=(0,410))
    ax.legend(title='Value source',loc='upper left',bbox_to_anchor=(1.01,1));fig.tight_layout();plt.show()


def same_day_correlations_plot(results):
    fig,axes=plt.subplots(1,2,figsize=(11,4))
    d=results.set_index('pollutant').rename(index={'pm25_ug_m3':'PM2.5','no2_ug_m3':'NO₂','so2_ug_m3':'SO₂'})
    for ax,cols,title in zip(axes,[['EPA temp','Meteostat temp'],['EPA humidity','Meteostat humidity']],['Temperature','Humidity']):
        d[cols].plot.bar(ax=ax,color=[EPA,METEO],rot=0)
        ax.axhline(0,color='#666666',linewidth=.7)
        ax.set(title=title,ylabel='Pearson correlation',xlabel='',ylim=(-.75,.35))
        ax.legend(handles=ax.containers,labels=['EPA','Meteostat'],loc='upper right',fontsize=9)
    fig.suptitle('Same dates, different weather source: does the pollutant relationship change?')
    fig.tight_layout();plt.show()
