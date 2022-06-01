# api.py
from requests import get
from datetime import datetime



class Watty:
    def __init__(self, country: str = "de") -> None:
        if country == "de":
            self._url = "https://api.awattar.de/v1/marketdata"
        elif country == "at":
            self._url = "https://api.awattar.at/v1/marketdata"
        else:
            # raise unknown country code error
            pass

    def request(self, start_timestamp: str = None, end_timestamp: str = None) -> list:
        """Requests prices

        Args:
            start_timestamp (str, optional): Epochseconds incl. milliseconds. Defaults to None.
            end_timestamp (str, optional): Epochseconds incl. milliseconds. Defaults to None.

        Returns:
            list: List of Price objects
        """
        if start_timestamp is not None or end_timestamp is not None:
            parameters = {
            "start_timestamp": start_timestamp,
            "end_timestamp": end_timestamp
            }
            res = get(self._url, params=parameters)
        else:
            res = get(self._url)

        prices = []

        if res.status_code == 200:
            for price in res.json()["data"]:
                prices.append(Price(price))
        
        return prices

class Price:
    """
    Wrapper around one price entry in an aWATTar response.

    Properties:
        .marketprice, .unit, .start_timestamp, .end_timestamp
    """
    def __init__(self, response: dict) -> None:
        self._response = response

    @property
    def marketprice(self) -> float:
        """Get the marketprice

        Returns:
            float: Marketprice
        """
        return self._response["marketprice"]

    @property
    def unit(self) -> str:
        """Get the unit

        Returns:
            str: Unit. Standard: Eur/Mwh
        """
        return self._response["unit"]

    @property
    def start_timestamp(self) -> int:
        """Get the start_timestamp

        Returns:
            str: Timestamp in Epochseconds incl. milliseconds.
        """
        return self._response["start_timestamp"]

    @property
    def end_timestamp(self) -> int:
        """Get the end_timestamp

        Returns:
            str: Timestamp in Epochseconds incl. milliseconds.
        """
        return self._response["end_timestamp"]

    @property
    def start_date(self) -> datetime:
        return self._epoch_to_date(self.start_timestamp/1000)

    @property
    def end_date(self) -> datetime:
        return self._epoch_to_date(self.end_timestamp/1000)
    
    def to_dict(self) -> dict:
        """Get the full response as dictionary

        Returns:
            dict: Response
        """
        return self._response
    
    def _epoch_to_date(self, epoch: int) -> datetime:
        return datetime.utcfromtimestamp(epoch)


def get_prices(country: str = "de", start_timestamp = None, end_timestamp = None) -> list:
    """Wrapper arount the Watty.request method.

    Args:
        country (str, optional): Country to get prices from ("de" or "at"). Defaults to "de".
        start_timestamp (_type_, optional): Epochseconds incl. milliseconds. Defaults to None.
        end_timestamp (_type_, optional): Epochseconds incl. milliseconds. Defaults to None.

    Returns:
        list: List of Price objects
    """
    if country == "de" or country == "at":
        watty = Watty(country)
    else:
        # raise UnknownCountryCodeError
        exit()
    
    if start_timestamp is not None or end_timestamp is not None:
        price_list = watty.request(start_timestamp, end_timestamp)
    else:
        price_list = watty.request()

    return price_list