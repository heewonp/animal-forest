import re
import logging
import pandas as pd
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DateUtils:
    """날짜 관련 유틸리티 함수 클래스"""
    
    @staticmethod
    def convert_date_columns(df, format='%Y%m%d'):
        """
        데이터프레임에서 날짜 형식의 컬럼을 datetime 타입으로 변환
        
        Parameters:
        df (pandas.DataFrame): 처리할 데이터프레임
        format (str): 날짜 형식 (기본: %Y%m%d)
        
        Returns:
        pandas.DataFrame: 날짜 컬럼이 변환된 데이터프레임
        """
        df_copy = df.copy()
        date_columns = [col for col in df_copy.columns if 'dt' in col.lower()]
        
        for col in date_columns:
            try:
                df_copy[col] = pd.to_datetime(df_copy[col], format=format)
                logger.info(f"날짜 컬럼 변환 완료: {col}")
            except Exception as e:
                logger.warning(f"{col} 컬럼 날짜 변환 실패: {e}")
        
        return df_copy
    
    @staticmethod
    def extract_time_components(df, date_column):
        """
        날짜 컬럼에서 연도, 월, 요일 등의 구성요소 추출
        
        Parameters:
        df (pandas.DataFrame): 처리할 데이터프레임
        date_column (str): 날짜 컬럼명
        
        Returns:
        pandas.DataFrame: 추출된 시간 구성요소가 추가된 데이터프레임
        """
        df_copy = df.copy()
        
        if date_column in df_copy.columns:
            # 날짜 컬럼이 datetime 형식인지 확인
            if pd.api.types.is_datetime64_any_dtype(df_copy[date_column]):
                # 연도, 월, 요일 추출
                df_copy[f'{date_column.replace("_dt", "")}_year'] = df_copy[date_column].dt.year
                df_copy[f'{date_column.replace("_dt", "")}_month'] = df_copy[date_column].dt.month
                df_copy[f'{date_column.replace("_dt", "")}_day'] = df_copy[date_column].dt.day
                df_copy[f'{date_column.replace("_dt", "")}_weekday'] = df_copy[date_column].dt.weekday
                df_copy[f'{date_column.replace("_dt", "")}_dayofweek'] = df_copy[date_column].dt.day_name()
                
                # 계절 추출
                month = df_copy[date_column].dt.month
                # 계절 매핑: 봄(3-5), 여름(6-8), 가을(9-11), 겨울(12-2)
                season_dict = {
                    1: '겨울', 2: '겨울', 3: '봄', 4: '봄', 5: '봄',
                    6: '여름', 7: '여름', 8: '여름', 9: '가을', 10: '가을',
                    11: '가을', 12: '겨울'
                }
                df_copy[f'{date_column.replace("_dt", "")}_season'] = month.map(season_dict)
                
                logger.info(f"{date_column} 컬럼에서 시간 구성요소 추출 완료")
            else:
                logger.warning(f"{date_column} 컬럼이 datetime 형식이 아닙니다.")
        else:
            logger.warning(f"{date_column} 컬럼이 데이터프레임에 존재하지 않습니다.")
        
        return df_copy

class TextUtils:
    """텍스트 처리 관련 유틸리티 함수 클래스"""
    
    @staticmethod
    def extract_weight(weight_str):
        """
        무게 문자열에서 숫자 추출
        
        Parameters:
        weight_str: 무게를 포함한 문자열
        
        Returns:
        float: 추출된 무게 값 (실패시 np.nan)
        """
        if pd.isna(weight_str):
            return np.nan
        try:
            weight = re.findall(r'([\d\.]+)', str(weight_str))
            return float(weight[0]) if weight else np.nan
        except:
            return np.nan
    
    @staticmethod
    def extract_breed(value):
        """
        품종 정보 추출
        
        Parameters:
        value: 품종 정보가 포함된 문자열
        
        Returns:
        str: 추출된 품종 정보
        """
        if pd.isna(value):
            return None
        value_str = str(value)
        
        # 대괄호 안의 내용을 제거하고 남은 부분을 품종으로 간주
        match = re.search(r'\](.*?)($|\s*\()', value_str)
        if match:
            breed = match.group(1).strip()
            return breed if breed else None
        
        # 대괄호가 없는 경우 다른 패턴 시도
        match = re.search(r'(개|고양이|축종)\s+(.*?)($|\s*\()', value_str)
        if match:
            return match.group(2).strip()
        
        return None

class LocationUtils:
    """지역 관련 유틸리티 함수 클래스"""
    
    @staticmethod
    def extract_sido_sigungu(address):
        """
        주소에서 시도와 시군구 부분만 추출하는 함수
        
        Args:
            address (str): 한국 주소
            
        Returns:
            tuple: (시도, 시군구)
        """
        if pd.isna(address):
            return ('미상', '미상')
            
        # 괄호 제거
        clean_address = re.sub(r'\([^)]*\)', '', str(address)).strip()
        
        # 시도 패턴 (서울특별시, 경기도, 세종특별자치시 등)
        sido_pattern = r'^(서울특별시|부산광역시|대구광역시|인천광역시|광주광역시|대전광역시|울산광역시|세종특별자치시|경기도|강원도|충청북도|충청남도|전라북도|전라남도|경상북도|경상남도|제주특별자치도)'
        
        # 시도 추출
        sido_match = re.match(sido_pattern, clean_address)
        sido = sido_match.group(1) if sido_match else '미상'
        
        if sido_match:
            remaining = clean_address[len(sido_match.group(1)):].strip()
        else:
            remaining = clean_address
        
        # 시군구 추출 (첫 번째 공백까지)
        sigungu = remaining.split()[0] if remaining and ' ' in remaining else remaining
        
        # 세종특별자치시는 시군구가 없으므로 특별 처리
        if sido == '세종특별자치시':
            return sido, ''
        
        return sido, sigungu
    
    @staticmethod
    def apply_to_dataframe(df, address_column):
        """
        데이터프레임의 주소 컬럼에서 시도와 시군구를 추출하여 새 컬럼으로 추가
        
        Args:
            df (pandas.DataFrame): 주소 컬럼이 있는 데이터프레임
            address_column (str): 주소가 있는 컬럼 이름
            
        Returns:
            pandas.DataFrame: 시도와 시군구 컬럼이 추가된 데이터프레임
        """
        df_copy = df.copy()
        
        # 주소 컬럼이 없는 경우 오류 처리
        if address_column not in df_copy.columns:
            logger.error(f"컬럼 '{address_column}'이 데이터프레임에 존재하지 않습니다.")
            return df_copy
        
        # 시도와 시군구 추출하여 새 컬럼 추가
        df_copy[['sido', 'sigungu']] = df_copy[address_column].apply(lambda x: pd.Series(LocationUtils.extract_sido_sigungu(x)))
        
        # 권역 분류 추가
        df_copy['region'] = df_copy['sido'].apply(LocationUtils.categorize_region)
        
        logger.info(f"{address_column} 컬럼에서 지역정보 추출 완료")
        return df_copy
    
    @staticmethod
    def categorize_region(sido):
        """
        시도를 권역별로 분류
        
        Parameters:
        sido: 시도명
        
        Returns:
        str: 권역 분류 (수도권, 영남권, 호남권, 충청권, 강원/제주)
        """
        capital_area = ['서울특별시', '인천광역시', '경기도']
        yeongnam = ['부산광역시', '대구광역시', '울산광역시', '경상북도', '경상남도']
        honam = ['광주광역시', '전라북도', '전라남도']
        chungcheong = ['대전광역시', '세종특별자치시', '충청북도', '충청남도']
        others = ['강원도', '제주특별자치도']
        
        if sido in capital_area:
            return '수도권'
        elif sido in yeongnam:
            return '영남권'
        elif sido in honam:
            return '호남권'
        elif sido in chungcheong:
            return '충청권'
        elif sido in others:
            return '강원/제주'
        else:
            return '기타'