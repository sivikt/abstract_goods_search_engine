import './App.css';
import 'react-table/react-table.css'
import React from 'react';
import ReactTable from 'react-table'
import { MDBContainer, MDBInputGroup, MDBInput, MDBBtn } from "mdbreact";
import Spinner from 'react-spinner-material';

class App extends React.Component {

  constructor(props) {
    super(props);

    this.state = {
        isDebug: new URLSearchParams(window.location.search).get('debug') === 'true',
        secretKey: new URLSearchParams(window.location.search).get('key'),
        loading: false,
        searchQuery: '',
        size: 1000,
        searchResults: {
            total_matched: 0,
            findings: []
        }
    };

    this.search = this.search.bind(this);
    this.updateSearchQuery = this.updateSearchQuery.bind(this);
    this.updateResultsSize = this.updateResultsSize.bind(this);

//    this.data= [{
//			"MaterialSerialNumber": "72271571",
//			"GoodsId": "W",
//			"GoodandService": "[ LAUNCHING AND HANDLING EQUIPMENT FOR MISSILES, SUCH AS ANTI-AIRCRAFT MISSILES ]",
//			"GoodsStatusClass": 2,
//			"GoodsRefsCount": 48,
//			"GoodsDeadCount": 399,
//			"GoodsLiveMinMaxNorm": 0.02171945701357466,
//			"ClassesFract": 0.14035087719298245,
//			"OwnerName": "WESTINGHOUSE ELECTRIC CORPORATION",
//			"OwnerAddress": "51 West 52nd Street, New York, NY, 10019, ",
//			"GoodsProducer": "Kaydi Osowski",
//			"StatusDesc": "REGISTERED AND RENEWED",
//			"Classes": "(009) Scientific, nautical, surveying, photographic, cinematographic, optical, weighing, measuring, signalling, checking (supervision), life-saving and teaching apparatus and instruments; apparatus and instruments for conducting, switching, transforming, accumulating, regulating or controlling electricity; apparatus for recording, transmission or reproduction of sound or images; magnetic data carriers, recording discs; automatic vending machines and mechanisms for coin operated apparatus; cash registers, calculating machines, data processing equipment and computers; fire extinguishing apparatus.\n(021) Household or kitchen utensils and containers; combs and sponges; brushes (except paint brushes); brush-making materials; articles for cleaning purposes; steel-wool; unworked or semi-worked glass (except glass used in building); glassware, porcelain and earthenware not included in other classes. \n(023) Yarns and threads, for textile use. \n(026) Lace and embroidery, ribbons and braid; buttons, hooks and eyes, pins and needles; artificial flowers. \n(029) Meat, fish, poultry and game; meat extracts; preserved, frozen, dried and cooked fruits and vegetables; jellies, jams, compotes; eggs, milk and milk products; edible oils and fats. \n(034) Tobacco; smokers' articles; matches. \n(036) Insurance; financial affairs; monetary affairs; real estate affairs. \n(044) Medical services; veterinary services; hygienic and beauty care for human beings or animals; agriculture, horticulture and forestry services. ",
//			"GoodsDeadMinMaxNorm": 0.023232793758006288,
//			"meta": {
//				"_score": 22.394129,
//				"_sort": 28.262965654310758
//			}
//		},
//		{
//			"MaterialSerialNumber": "72111032",
//			"GoodsId": "W",
//			"GoodandService": "[Laminated Plastic Materials-Namely, Sheet, Tube, Industrial Plate, Copper Clad and Other Plastic Shapes, and Synthetic Resins]",
//			"GoodsStatusClass": 2,
//			"GoodsRefsCount": 48,
//			"GoodsDeadCount": 399,
//			"GoodsLiveMinMaxNorm": 0.02171945701357466,
//			"ClassesFract": 0.12280701754385966,
//			"OwnerName": "WESTINGHOUSE ELECTRIC CORPORATION",
//			"OwnerAddress": "51 West 52nd Street, New York, NY, 10019, ",
//			"GoodsProducer": "Kaydi Osowski",
//			"StatusDesc": "STATEMENT OF CONTINUED USE ACCEPTED IN PART",
//			"Classes": "(001) Chemicals used in industry, science and photography, as well as in agriculture, horticulture and forestry; unprocessed artificial resins; unprocessed plastics; manures; fire extinguishing compositions; tempering and soldering preparations; chemical substances for preserving foodstuffs; tanning substances; adhesives used in industry. \n(014) Precious metals and their alloys and goods in precious metals or coated therewith, not included in other classes; jewelry, precious stones; horological and chronometric instruments.\n(015) Musical instruments.\n(021) Household or kitchen utensils and containers; combs and sponges; brushes (except paint brushes); brush-making materials; articles for cleaning purposes; steel-wool; unworked or semi-worked glass (except glass used in building); glassware, porcelain and earthenware not included in other classes. \n(023) Yarns and threads, for textile use. \n(026) Lace and embroidery, ribbons and braid; buttons, hooks and eyes, pins and needles; artificial flowers. \n(034) Tobacco; smokers' articles; matches. ",
//			"GoodsDeadMinMaxNorm": 0.023232793758006288,
//			"meta": {
//				"_score": 22.394129,
//				"_sort": 27.87008619876185
//			}
//		},
//		{
//			"MaterialSerialNumber": "71003264",
//			"GoodsId": "W",
//			"GoodandService": "[ SHOT-SHELLS, ] CARTRIDGES [ , AND PRIMERS ]",
//			"GoodsStatusClass": 2,
//			"GoodsRefsCount": 258,
//			"GoodsDeadCount": 529,
//			"GoodsLiveMinMaxNorm": 0.1167420814479638,
//			"ClassesFract": 0.017543859649122806,
//			"OwnerName": "OLIN CORPORATION",
//			"OwnerAddress": "190 Carondelet Plaza, Suite 1530, St. Louis, MO, 63105, ",
//			"GoodsProducer": "Bryan K. Wheelock",
//			"StatusDesc": "REGISTERED AND RENEWED",
//			"Classes": "(009) Scientific, nautical, surveying, photographic, cinematographic, optical, weighing, measuring, signalling, checking (supervision), life-saving and teaching apparatus and instruments; apparatus and instruments for conducting, switching, transforming, accumulating, regulating or controlling electricity; apparatus for recording, transmission or reproduction of sound or images; magnetic data carriers, recording discs; automatic vending machines and mechanisms for coin operated apparatus; cash registers, calculating machines, data processing equipment and computers; fire extinguishing apparatus.",
//			"GoodsDeadMinMaxNorm": 0.030802375684173752,
//			"meta": {
//				"_score": 22.394129,
//				"_sort": 27.640758354214093
//			}
//		},
//		{
//			"MaterialSerialNumber": "73034497",
//			"GoodsId": "W",
//			"GoodandService": "COMPONENTS OF AMMUNITION-NAMELY, [ PRIMERS, BULLETS, AND ] CARTRIDGE CASES",
//			"GoodsStatusClass": 2,
//			"GoodsRefsCount": 258,
//			"GoodsDeadCount": 529,
//			"GoodsLiveMinMaxNorm": 0.1167420814479638,
//			"ClassesFract": 0.017543859649122806,
//			"OwnerName": "OLIN CORPORATION",
//			"OwnerAddress": "190 Carondelet Plaza, Suite 1530, St. Louis, MO, 63105, ",
//			"GoodsProducer": "Bryan K. Wheelock",
//			"StatusDesc": "REGISTERED AND RENEWED",
//			"Classes": "(013) Firearms; ammunition and projectiles; explosives; fireworks.",
//			"GoodsDeadMinMaxNorm": 0.030802375684173752,
//			"meta": {
//				"_score": 22.394129,
//				"_sort": 27.640758354214093
//			}
//		}]
  }

  search() {
    this.setState({loading: true});

    var url = new URL("http://tmelasticsearch.westus2.cloudapp.azure.com:8080/search"),
    params = {q:this.state.searchQuery, size:this.state.size}
    Object.keys(params).forEach(key => url.searchParams.append(key, params[key]))

    fetch(url, {
          method: 'get',
          headers: new Headers({
             'Authorization': 'Basic '+ this.state.secretKey
          })
      })
      .then(response => response.json())
      .then(responseData => {
          this.setState({
            loading: false,
            searchResults:responseData
          })
      });
  }

  updateSearchQuery(event) {
    this.setState({searchQuery: event.target.value});
  }

  updateResultsSize(event) {
    var sz = isNaN(event.target.value) || (event.target.value < 1) ? 100 : event.target.value;
    this.setState({size: sz});
  }

  render() {
    const columns = [{
        id: "row",
        Header: '',
        filterable: false,
        Cell: (row) => <div>{row.index}</div>,
        width: 80
      },{
        Header: 'Material',
        accessor: 'MaterialNumber',
        Cell: props => <span class='small-text'>{props.value}</span>,
        width: 110
      }, {
        Header: 'Goods Name',
        accessor: 'GoodsId',
        Cell: props => <span class='small-text'>{props.value}</span>,
        style: { 'white-space': 'unset' },
        width: 240
      }, {
        id: "owner_info",
        Header: 'Owner Name & Address',
        accessor: d => d.OwnerName,
        Cell: props => <span class='small-text'>{props.value}</span>,
        style: { 'white-space': 'unset' },
        width: 200
      }, {
        Header: 'Goods Producer',
        accessor: 'GoodsProducer',
        Cell: props => <span class='small-text'>{props.value}</span>,
        style: { 'white-space': 'unset' },
        width: 200
      }, {
        Header: 'Current Status',
        accessor: 'StatusDesc',
        Cell: props => <span class='small-text'>{props.value}</span>,
        style: { 'white-space': 'unset' },
        width: 150
      }, {
        Header: 'Class(es)',
        accessor: 'Classes',
        Cell: props => <span class='small-text'>{props.value}</span>,
        style: { 'white-space': 'unset' },
        width: 510
      }, {
        Header: 'Good and Service',
        accessor: 'GoodandService',
        Cell: props => <span class='small-text'>{props.value}</span>,
        style: { 'white-space': 'unset' },
        width: 200
      }, {
        Header: 'Status',
        accessor: 'GoodsStatusClass',
        show: this.state.isDebug,
        width: 70
      }, {
        Header: 'Refs Count',
        accessor: 'GoodsRefsCount',
        Cell: props => <span class='number small-text'>{props.value}</span>,
        show: this.state.isDebug,
        width: 100
      }, {
        Header: 'Dead Count',
        accessor: 'GoodsDeadCount',
        Cell: props => <span class='number small-text'>{props.value}</span>,
        show: this.state.isDebug,
        width: 100
      }, {
        Header: 'Classes Norm',
        accessor: 'ClassesFract',
        Cell: props => <span class='number small-text'>{props.value.toFixed(4)}</span>,
        show: this.state.isDebug,
        width: 120
      }, {
        Header: 'Live Norm',
        accessor: 'GoodsLiveMinMaxNorm',
        Cell: props => <span class='number small-text'>{props.value.toFixed(4)}</span>,
        show: this.state.isDebug,
        width: 100
      }, {
        Header: 'Dead Norm',
        accessor: 'GoodsDeadMinMaxNorm',
        Cell: props => <span class='number small-text'>{props.value.toFixed(4)}</span>,
        show: this.state.isDebug,
        width: 100
      }, {
        id: 'rawScore',
        Header: 'Raw Score',
        accessor: d => d.meta._score,
        Cell: props => <span class='number small-text'>{props.value.toFixed(4)}</span>,
        show: this.state.isDebug,
        width: 120
      }, {
        id: 'score',
        Header: 'Score',
        accessor: d => d.meta._sort,
        Cell: props => <span class='number small-text'>{props.value.toFixed(4)}</span>,
        show: this.state.isDebug,
        width: 120
    }]

    const sortable = false;
    const pageSizes = [5, 10, 20, 25, 50, 100, 1000, 5000, 10000];

    return (
      <div class="App p-3">
        <div style={{display: "flex", visibility: this.state.loading ? "visible" : "hidden", justifyContent: "center", alignItems: "center", position: "absolute", width: "100%", height: "100%"}}>
            <Spinner size={120} spinnerColor={"#333"} spinnerWidth={2} visible={this.state.loading} />
        </div>
        <div class="search-box">
            <MDBContainer>
                <div className="w-25">
                    <MDBInput
                      hint="max results to return (default 1000)"
                      containerClassName="mb-3"
                      type="number"
                      onChange={this.updateResultsSize}
                    />
                </div>

                <div className="w-50">
                    <MDBInputGroup
                      hint="search for"
                      containerClassName="mb-3"
                      onChange={this.updateSearchQuery}
                      append={
                        <MDBBtn color="success" className="m-0" onClick={this.search}>
                          GO!
                        </MDBBtn>
                      }
                    />
                 </div>
            </MDBContainer>
        </div>
        <div class="search-list">
           <div style={{padding: "10px 0px"}}>{this.state.searchResults.total_matched} goods found</div>
           <ReactTable
                sortable={sortable}
                pageSizeOptions={pageSizes}
                data={this.state.searchResults.findings}
                columns={columns}
           />
        </div>
     </div>
    );
  }
}

export default App;
