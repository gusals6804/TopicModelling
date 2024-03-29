from konlpy.tag import Kkma, Okt
from pandas import DataFrame as df
import pandas as pd
import time
import re
import os

kkma = Kkma()
ex = '우한 폐렴 공포    신종 코로나바이러스 감염증우한 폐렴 확산으로 중국 경제가 지난 2003년' \
     ' 사스·중증급성호흡기증후군 발병 당시 때보다 더 큰 충격을 받을 수 있다는 한국은행의 전망이 나왔다 ' \
     '2일 한국은행의 해외경제포커스 2003년 사스 발병 당시 및 현재 중국경제 여건 보고서에 따르면 신종 ' \
     '코로나바이러스 감염증이 중국 경제에 부정적 영향을 줄 것이란 분석이 나왔다 사스 때보다 빠른 확산세 ' \
     '약해진 경제 회복력 등이 중국 경제의 하방 리스크 요인으로 지목됐다 신종코로나 전개 상황의 불확실성이 ' \
     '높아 단기적으로 중국 경제가 서비스업을 중심으로 타격을 받고 확산이 장기화하면 제조업 등에도 부정적인 영향을 ' \
     '받을 것으로 분석됐다 사스 사태 여파가 컸던 2003년 2분기 중국 경제성장률은 91로 전분기111보다 2포인트 하락했다 ' \
     '교통·운수업이 54포인트 숙박·음식업이 36포인트 떨어지는 등 여행·숙박 소매업 등이 주로 위축된 영향이 컸다 ' \
     '그러나 중국경제는 사스 발병 당시 2003년 2분기를 중심으로 일부 영향을 받았으나 곧 회복되면서 10대의 높은 성장세를 시현했다'
nouns = kkma.nouns(ex)
clean_noun = []

for noun in nouns:
    noun = re.sub('\\d', '', noun)
    if len(noun) > 1:
        clean_noun.append(noun)
print(clean_noun)